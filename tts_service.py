import os

def generate_tts_audio(text: str, voice: str) -> str:
    murf_key = os.getenv("MURF_API_KEY")
    if not murf_key:
        raise ValueError("MURF_API_KEY not set")
    # TODO: Integrate Murf.ai request here.
    
    safe_text = text.strip().replace(" ", "_")[:60]
    return f"https://example.com/audio/{voice}_{safe_text}.mp3"
