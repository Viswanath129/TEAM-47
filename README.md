# 🎓 ClassPulse AI

## 📖 Project Overview

**ClassPulse AI** is a cutting-edge educational technology solution designed to optimize the lecture feedback loop. 

By leveraging **Edge AI (Local Large Language Models)**, the application transcribes and analyzes classroom audio in real-time without relying on external servers for intelligence. This ensures zero-latency performance and absolute data privacy. The system follows a **Hybrid Architecture**, processing data locally for immediate feedback while syncing structured insights to a cloud backend for long-term analytics.

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
* **Zero-Latency Transcription:** Utilizes local speech-to-text engines to transcribe lectures instantly.
* **On-Device Analysis:** Runs quantized LLMs (e.g., Llama 3, Mistral) locally via Ollama to generate summaries and quizzes without internet access.
* **Data Sovereignty:** Audio data is processed entirely on the client machine; it never leaves the device.

### ☁️ Cloud Synchronization (Online Mode)
* **Seamless Sync:** Automatically pushes structured data (lecture notes, quiz scores) to **Supabase/Firebase** when connectivity is restored.
* **Role-Based Access:** Distinct portals for **Instructors** (analytics, management) and **Students** (quizzes, history).
* **Long-Term Analytics:** Visualizes comprehension trends over the semester.

### 🎨 User Experience
* **Adaptive UI:** Dark-mode enabled, responsive interface built with Tailwind CSS.
* **Multilingual Support:** Native support for English and regional languages (Hindi, Telugu).
* **Automated Assessment:** Instantly generates and grades 10-question multiple-choice quizzes.

---

## 🛠️ Tech Stack

| Component | Technology Used | Description |
| :--- | :--- | :--- |
| **Frontend** | HTML, CSS, JS | High-performance UI library like tailwindcss and anime.js . |
| **Styling** | Tailwind CSS | Utility-first CSS framework for responsive design. |
| **Local AI** | Ollama | Runtime for running LLMs (Llama 3, Mistral) locally. |
| **Speech Engine** | Web Speech API / Whisper | Real-time audio capture and transcription. |
| **Backend (BaaS)** | Supabase / Firebase | Authentication, Real-time Database, and Storage. |
| **Version Control** | Git & GitHub | Source code management. |

---

## ⚙️ Setup & Installation

Follow these steps to deploy the application in a local development environment.

### Prerequisites
* **html, css, js** (latest version)
* **Ollama** (Installed and running)
* **Git**
