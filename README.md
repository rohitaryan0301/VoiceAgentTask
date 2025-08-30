# 🤖 Full-Stack AI Voice Agent

*A project for the 30 Days of AI Voice Agents Challenge*

This is a complete, real-time, conversational AI voice agent with a configurable UI, multiple personas, and advanced skills like web search and image generation. The entire application is deployed and accessible on the web.



---

### 🎥 Demo Screenshot

![Live Demo of the AI Voice Agent] https://github.com/rohitaryan0301/VoiceAgentTask/blob/main/Screenshot%202025-08-30%20111927.png

---

### 🔥 Key Features

- **Real-time Voice Conversation:** Fluid, low-latency conversation powered by WebSockets.
- **Dynamic UI Configuration:** Users can securely enter their own API keys directly in the browser, which are stored in `localStorage`.
- **Switchable Personas:** Choose from different agent personalities (like Helpful Assistant, Sarcastic Robot, etc.), which changes both the LLM's system prompt and the voice.
- **🧠 Advanced Skills (Tool Use):**
  - **🌐 Real-time Web Search:** Can answer questions about current events by searching the web with the Tavily API.
  - **🎨 AI Image Generation:** Can generate images from text descriptions using OpenAI's DALL-E 3 and display them in the UI.
- **Full-Stack Architecture:** Built with a Python/FastAPI backend and a Vanilla JavaScript frontend.
- **Cloud Deployed:** Fully deployed and accessible on the internet via Render.

---

### 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Gunicorn
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Real-time Communication:** WebSockets
- **Services & APIs:**
  - **Speech-to-Text:** Deepgram
  - **LLM & Tool Orchestration:** Google Gemini
  - **Text-to-Speech:** ElevenLabs
  - **Web Search Skill:** Tavily
  - **Image Generation Skill:** OpenAI DALL-E 3
- **Deployment:** Render, GitHub

---

### 🚀 How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/rohitaryan0301/VoiceAgentTask.git
    cd VoiceAgentTask
    ```

2.  **Setup the Backend:**
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    # .\venv\Scripts\activate    # On Windows
    pip install -r requirements.txt
    ```

3.  **Run the Backend Server:**
    *(Run this from the project's root directory)*
    ```bash
    uvicorn backend.main:app --host 0.0.0.0 --port 8000
    ```

4.  **Launch the Frontend:**
    - Open `http://localhost:8000` in your web browser.

---

### 🎤 How to Use the Deployed Agent

1.  **Visit the Live URL:** Go to the [Live Demo Link](#-live-demo-link) at the top of this README.
2.  **Configure Keys:** Click the settings (⚙️) icon and enter your API keys for all the required services.
3.  **Save and Start:** Save the keys and start the conversation. The agent is now ready to use!

---

*This project was built as part of the 30 Days of AI Voice Agents challenge. It demonstrates a complete pipeline from voice input to multi-skilled AI response and back to voice output.*