# 🎓 ClassPulse AI

## 📖 Project Overview

**ClassPulse AI** is a cutting-edge educational technology solution designed to optimize the lecture feedback loop. 

By leveraging **Edge AI (Local Large Language Models)** principles, the application transcribes and analyzes classroom audio in real-time. This ensures zero-latency performance and absolute data privacy. The system follows a **Hybrid Architecture**, processing data locally for immediate feedback while designed to sync structured insights to a cloud backend for long-term analytics.

---

## 📉 The Problem Statement

Traditional classroom environments face significant technological and pedagogical challenges:

* **⚠️ Connectivity Dependency:** Most AI tools require constant, high-speed internet, making them unreliable in remote or infrastructure-poor educational institutions.
* **🔒 Data Privacy Concerns:** Institutions are hesitant to stream sensitive classroom audio to third-party APIs for processing.
* **📉 Delayed Feedback Loops:** Instructors often lack immediate insight into student comprehension, realizing gaps in knowledge only after exams.
* **🐌 Latency:** Cloud-based transcription often introduces lags that disrupt the flow of real-time interaction.

---

## ✨ Key Features

### 🛡️ Edge Intelligence (Offline Mode)
* **Zero-Latency Transcription:** Utilizes the browser's native **Web Speech API** to transcribe lectures instantly.
* **On-Device Analysis:** Designed to run quantized LLMs (e.g., Llama 3, Mistral) locally to generate summaries and quizzes without internet access.
* **Data Sovereignty:** Audio data is processed entirely on the client machine; it never leaves the device.

### ☁️ Cloud Synchronization (Online Mode)
* **Seamless Sync:** Architecture supports pushing structured data (lecture notes, quiz scores) to **Supabase/Firebase** when connectivity is restored.
* **Role-Based Access:** Distinct portals for **Instructors** (analytics, management) and **Students** (quizzes, history).
* **Long-Term Analytics:** Visualizes comprehension trends over the semester.

### 🎨 User Experience
* **Adaptive UI:** Dark-mode enabled, responsive interface built with **Tailwind CSS**.
* **Multilingual Support:** Native support for **English (US/India)** and regional languages including **Hindi, Telugu, Tamil, Kannada, Spanish, French, and German**.
* **Automated Assessment:** Instantly generates and grades 10-question multiple-choice quizzes based on the lecture content.

---

## 🛠️ Tech Stack

| Component | Technology Used | Description |
| :--- | :--- | :--- |
| **Frontend** | html,css,js | Built using a lightweight single-file architecture via CDN for maximum portability. |
| **Styling** | Tailwind CSS | Utility-first CSS framework for rapid, responsive UI design. |
| **Speech Engine** | Web Speech API | Native browser API for real-time speech-to-text conversion. |
| **Compiler** | Babel | In-browser JSX compilation. |
| **Icons** | Lucide React | Clean, lightweight SVG icons. |
| **Local AI** | Ollama (Integration Ready) | Runtime for running LLMs (Llama 3, Mistral) locally. |

---

## ⚙️ Installation & Setup

This project uses a **Serverless/Buildless** architecture for the prototype, meaning you do not need `npm` or `node_modules` to run the interface.

### Prerequisites
* A modern web browser (Google Chrome, Microsoft Edge, or Brave recommended for best Speech API support).
* An internet connection (for the initial loading of CDN scripts).
