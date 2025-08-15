# 🎙️ AI Voice Agent — Day 14

An interactive AI Voice Agent built as part of the **#30DaysOfAIVoiceAgents** challenge.  
This project allows real-time voice conversations with AI, powered by **Murf.ai**, **Next.js**, and **FastAPI**.

---

## 🚀 Project Overview

The AI Voice Agent listens to the user, transcribes the audio, processes it through an AI model, and responds back in a **natural, human-like voice**.  
It combines **speech-to-text**, **natural language understanding**, and **text-to-speech** to create a seamless voice assistant experience.

---

## 🛠️ Technologies Used

- **Frontend**: Next.js + Tailwind CSS (optional)
- **Backend API**: FastAPI
- **AI & TTS**: Murf.ai API (placeholder)
- **Real-Time Communication**: WebSockets (can be added)
- **Transcription**: Whisper / Speech-to-Text models (optional)

---

## 🏗️ Architecture

```
User → Microphone → Frontend (Next.js) → Backend API (FastAPI)
     → Murf.ai API → AI Response → Text-to-Speech → Frontend → Speaker
```

---

## ✨ Features (example)

- 🎤 **Real-time voice input**
- 🧠 **AI-driven conversation**
- 🗣️ **Dynamic voice selection**
- ⏳ **Loading state indicators**
- 📷 **Screenshots support for documentation**

---

## 📦 What is included in this folder

- `README.md` (this file)
- `backend/` – minimal FastAPI server stub and `.env.example`
- `frontend/` – placeholder Next.js app with `pages/index.js` and `.env.local.example`
- `LICENSE` – MIT

> This is a skeleton to help you quickly run and test the structure. Replace the placeholders with your real implementation (Murf.ai calls, UI, transcription, etc).

---

## 🔑 Environment variables (examples)

**Backend `.env`**
```
MURF_API_KEY=your_murf_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

**Frontend `.env.local`**
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

---

## ▶️ Quick start (local)

1. Backend
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # or create .env and add keys
uvicorn main:app --reload --port 8000
```

2. Frontend
```bash
cd ../frontend
npm install
# create .env.local from .env.local.example and set NEXT_PUBLIC_API_BASE_URL
npm run dev
# open http://localhost:3000
```

---



