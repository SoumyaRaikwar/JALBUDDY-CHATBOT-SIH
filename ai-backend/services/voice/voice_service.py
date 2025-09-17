"""
Voice Service Stubs (ASR/TTS)
"""
from typing import Dict

class VoiceService:
    def transcribe(self, audio_bytes: bytes, language: str = "hi") -> Dict:
        return {"text": "<transcribed text>", "language": language, "engine": "whisper-stub"}

    def synthesize(self, text: str, language: str = "hi") -> Dict:
        return {"status": "ok", "engine": "bhashini-stub", "language": language}

