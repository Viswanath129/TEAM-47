from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import json
import re

app = FastAPI(title="ClassPulse AI Backend")

# ---------- Serve Frontend ----------
app.mount("/", StaticFiles(directory="../ui", html=True), name="ui")

# ---------- Models ----------
class NotesRequest(BaseModel):
    transcript: str

# ---------- Ollama Wrapper ----------
def ollama_infer(prompt: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    data = response.json()
    return data.get("response", "").strip()

# ---------- JSON Extractor ----------
def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found")
    return json.loads(match.group())

# ---------- API ----------
@app.post("/api/generate-notes")
def generate_notes(data: NotesRequest):
    prompt = f"""
You are an educational AI.

LECTURE:
{data.transcript}

Return STRICT JSON ONLY:
{{
  "notes": "Markdown formatted notes",
  "teacher_score": {{
    "score": 0-10,
    "simplicity": 0-10,
    "clarity": 0-10,
    "examples": 0-10,
    "feedback": "one sentence"
  }}
}}
"""

    raw = ollama_infer(prompt)

    try:
        parsed = extract_json(raw)
    except Exception:
        return {
            "error": "Invalid AI output",
            "raw": raw
        }

    return parsed
