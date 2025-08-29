import logging
from fastapi import FastAPI, HTTPException
from schemas.voice import TTSRequest, TTSResponse
from services.tts_service import generate_tts_audio

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger("voice-agent")

app = FastAPI(title="AI Voice Agent - Day 14 (Refactored)")

@app.get("/")
async def root():
    logger.info("Root endpoint hit")
    return {"status": "ok", "message": "Backend running (Day 14 Refactor)"}

@app.post("/tts", response_model=TTSResponse)
async def tts(req: TTSRequest):
    logger.info("TTS request received")
    try:
        audio_url = generate_tts_audio(req.text, req.voice)
        logger.info("TTS generated successfully")
        return TTSResponse(message="TTS generated successfully", audio_url=audio_url)
    except Exception as e:
        logger.exception("TTS generation failed")
        raise HTTPException(status_code=500, detail=str(e))

