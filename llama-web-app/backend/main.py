import os
import json
import re
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai

# -----------------------------
# PATH SETUP
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(_file_))
# Assumes 'ui' folder is one level up, adjust if index.html is in the same folder
UI_DIR = os.path.join(BASE_DIR, "..", "ui") 

# Fallback: If UI dir doesn't exist (e.g., flat structure), serve current dir
if not os.path.exists(UI_DIR):
    UI_DIR = BASE_DIR

# -----------------------------
# FASTAPI APP
# -----------------------------
app = FastAPI(title="ClassPulse AI Backend")

# Serve UI Static Files
app.mount("/static", StaticFiles(directory=UI_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    index_path = os.path.join(UI_DIR, "index.html")
    if not os.path.exists(index_path):
        return HTMLResponse("<h1>index.html not found. Ensure it is in the 'ui' folder or same folder.</h1>", status_code=404)
    return open(index_path, encoding="utf-8").read()

# -----------------------------
# GEMINI CONFIG
# -----------------------------
# API Key integrated
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyDPons4YpW58orxx041TLni_Ax_yocJ1R4"

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY is missing.")

genai.configure(api_key=GEMINI_API_KEY)

# List of models to try in order of preference
# Added more variants to ensure one works
MODELS_TO_TRY = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro", "gemini-1.0-pro"]

async def generate_with_fallback(prompt):
    last_error = None
    
    # Configure safety settings to avoid blocking educational content
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_ONLY_HIGH"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_ONLY_HIGH"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_ONLY_HIGH"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_ONLY_HIGH"
        },
    ]

    # 1. Try specific optimized models first
    for model_name in MODELS_TO_TRY:
        try:
            print(f"Attempting generation with model: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"},
                safety_settings=safety_settings
            )
            return response
        except Exception as e:
            print(f"Model {model_name} failed: {e}")
            last_error = e
            continue

    # 2. Dynamic Fallback: Find ANY valid model available to the key
    # This solves the "Model not found" error by asking Google what IS available
    print("Hardcoded models failed. Searching for available models...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                model_name = m.name
                print(f"Found dynamic model: {model_name}")
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(
                        prompt,
                        generation_config={"response_mime_type": "application/json"},
                        safety_settings=safety_settings
                    )
                    return response
                except Exception as inner_e:
                    print(f"Dynamic model {model_name} failed: {inner_e}")
                    last_error = inner_e
                    continue
    except Exception as list_e:
        print(f"Failed to list models: {list_e}")

    # If all models fail, raise the last error
    if last_error:
        raise last_error

def clean_json_response(text):
    """Cleans markdown code blocks from JSON string."""
    text = text.strip()
    if text.startswith("json"):
        text = text[7:]
    elif text.startswith(""):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

# -----------------------------
# REQUEST MODELS
# -----------------------------
class TranscriptRequest(BaseModel):
    text: str

# -----------------------------
# API ENDPOINT
# -----------------------------
@app.post("/api/generate-notes")
async def generate_notes(data: TranscriptRequest):
    if not data.text.strip():
        raise HTTPException(status_code=400, detail="Empty transcript")
    
    # Prompt designed to return the EXACT JSON structure your React frontend expects
    prompt = f"""
    You are an expert educational AI (ACIS). Analyze the following lecture text to create a high-quality study aid.
    
    Return a valid JSON object with exactly these keys:
    1. "notes": A comprehensive markdown string representing a study guide.
        - *MANDATORY*: Start with a section titled "## 📊 Analysis & Statistics" that includes:
            - *Understandability*: A brief assessment of how easy the text is to understand.
            - *Stats*: Word count (approx), Estimated Reading Time.
            - *Topic Coverage*: List of main topics covered in the text.
        - Follow with standard sections: ## Executive Summary, ## Key Concepts, ## Detailed Breakdown.
        - Use headers (##), bullet points, and bold text for formatting.
    2. "teacher_score": An object evaluating the input text quality:
        - "score" (number 1-10, reflect overall quality), 
        - "simplicity" (1-10), 
        - "clarity" (1-10), 
        - "examples" (1-10), 
        - "feedback" (string, detailed constructive feedback on how to improve the explanation, what is missing, and improvement features).
    3. "flashcards": An array of 5 to 10 objects, each having "term" and "definition".
    4. "quiz": An array of objects. Generate *5 to 10 questions* based on the content length and density.
        - Focus on covering *ALL important topics* mentioned.
        - Logic: Test application/analysis, not just definition recall.
        - Each object must have: 
            - "id" (unique string/number)
            - "question" (string)
            - "options": Array of 4 objects {{"text": "...", "type": "correct"|"distractor"|"misconception"}}
            - "correctAnswer" (string matching the correct option text)
            - "concept" (string, the concept being tested)
            - "isRemediation" (boolean, false)
            - "explanation" (string, explaining the answer)

    Lecture Text:
    {data.text}
    """

    try:
        # Request JSON response with fallback logic
        response = await generate_with_fallback(prompt)
        
        # Clean and Parse the JSON string
        cleaned_text = clean_json_response(response.text)
        response_data = json.loads(cleaned_text)
        
        return response_data

    except Exception as e:
        print(f"All models failed. Final error: {e}")
        # Return a JSON error that the frontend can display nicely
        return JSONResponse(
            status_code=500,
            content={"error": f"AI Generation failed: {str(e)}"}
        )
