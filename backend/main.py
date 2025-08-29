import os
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import google.generativeai as genai
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
from openai import OpenAI as OpenAIClient
from elevenlabs.client import ElevenLabs
from tavily import TavilyClient

load_dotenv()
app = FastAPI()

# --- TOOL AND PERSONA DEFINITIONS ---
PERSONAS = {"assistant": "You are a helpful AI assistant.", "robot": "You are a sarcastic robot.", "pirate": "You are a gruff, old pirate."}
PERSONA_VOICES = {"assistant": "Rachel", "robot": "Arnold", "pirate": "Adam"}
AGENT_TOOLS = {"function_declarations": [{"name": "web_search", "description": "Performs a web search.", "parameters": {"type": "object", "properties": {"query": {"type": "string", "description": "The search query"}}}}, {"name": "generate_image", "description": "Generates an image from a description.", "parameters": {"type": "object", "properties": {"prompt": {"type": "string", "description": "A detailed image description."}}}}]}

class ConnectionManager:
    # Day 27 से ConnectionManager क्लास में कोई बदलाव नहीं
    def __init__(self, websocket: WebSocket, persona: str):
        self.websocket = websocket
        self.persona = persona
        self.deepgram_client = None
        self.elevenlabs_client = None
        self.tavily_client = None
        self.openai_dalle_client = None
        self.chat_session = None
        self.deepgram_connection = None

    async def initialize_clients(self, keys: dict):
        try:
            self.deepgram_client = DeepgramClient(keys["deepgram"])
            self.elevenlabs_client = ElevenLabs(api_key=keys["elevenlabs"])
            self.tavily_client = TavilyClient(api_key=keys["tavily"])
            self.openai_dalle_client = OpenAIClient(api_key=keys["openai"])
            genai.configure(api_key=keys["gemini"])
            
            system_prompt = PERSONAS.get(self.persona, PERSONAS["assistant"])
            model = genai.GenerativeModel('gemini-1.5-pro-latest', system_instruction=system_prompt, tools=AGENT_TOOLS)
            self.chat_session = model.start_chat()
        except Exception as e:
            await self.websocket.close(code=1011, reason=f"API Key initialization failed: {e}")

    async def start_deepgram_transcription(self):
        self.deepgram_connection = self.deepgram_client.listen.asynclive.v("1")
        self.deepgram_connection.on(LiveTranscriptionEvents.Transcript, self.on_deepgram_message)
        options = LiveOptions(model="nova-2", language="en-US", smart_format=True)
        await self.deepgram_connection.start(options)

    async def on_deepgram_message(self, _, result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if len(transcript) > 0:
            audio_stream = await self.get_llm_response(transcript)
            if audio_stream:
                for chunk in audio_stream:
                    if chunk: await self.websocket.send_bytes(chunk)
            await self.websocket.send_text('{"status": "tts_finished"}')

    async def get_llm_response(self, text: str):
        try:
            response = await self.chat_session.send_message_async(text)
            function_call = response.candidates[0].content.parts[0].function_call
            if function_call:
                tool_response_text = ""
                if function_call.name == "web_search":
                    results = self.tavily_client.search(query=function_call.args["query"], search_depth="basic", max_results=3)
                    tool_response_text = "\n".join([f"{res['title']}: {res['content']}" for res in results['results']])
                elif function_call.name == "generate_image":
                    dalle_response = self.openai_dalle_client.images.generate(model="dall-e-3", prompt=function_call.args["prompt"], n=1, size="1024x1024")
                    image_url = dalle_response.data[0].url
                    await self.websocket.send_text(f'{{"type": "image", "url": "{image_url}"}}')
                    tool_response_text = "Image was created and sent to the user."
                response = await self.chat_session.send_message_async(
                    [genai.types.FunctionResponse(name=function_call.name, response={"result": tool_response_text})]
                )
            assistant_response = response.text
            voice_name = PERSONA_VOICES.get(self.persona, PERSONA_VOICES["assistant"])
            return self.elevenlabs_client.generate(text=assistant_response, voice=voice_name, model="eleven_multilingual_v2", stream=True)
        except Exception as e: return None

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, persona: str = "assistant"):
    await websocket.accept()
    manager = ConnectionManager(websocket, persona)
    try:
        config_message = await websocket.receive_json()
        if config_message.get("type") == "config":
            await manager.initialize_clients(config_message["keys"])
            await manager.start_deepgram_transcription()
        else: raise ValueError("Config message required.")
        while True:
            data = await websocket.receive_bytes()
            if manager.deepgram_connection: await manager.deepgram_connection.send(data)
    except (WebSocketDisconnect, ConnectionError, ValueError): pass
    finally:
        if manager.deepgram_connection: await manager.deepgram_connection.finish()

# DEPLOYMENT CODE: Serve Frontend Files
frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
@app.get("/")
async def read_root(): return FileResponse(os.path.join(frontend_dir, 'index.html'))
app.mount("/", StaticFiles(directory=frontend_dir), name="static")