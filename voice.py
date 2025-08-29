from pydantic import BaseModel

class TTSRequest(BaseModel):
    text: str
    voice: str = "default"

class TTSResponse(BaseModel):
    message: str
    audio_url: str
