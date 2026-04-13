import os
from groq import Groq
from core.config import groq_api_key

client = Groq(api_key=groq_api_key)

def transcribe_audio(file_path: str) -> str:
    try:
        with open(file_path, "rb") as file:
            # whisper api call
            transcription = client.audio.transcriptions.create(
                file=(file_path, file.read()),
                model="whisper-large-v3-turbo",
                response_format="verbose_json",
            )

        text = transcription.text
        lang = transcription.language

        if not text.strip():
            return "empty audio."

        # returning formatted lowercase result
        return f"[{lang}] {text.strip()}".lower()

    except Exception as e:
        return f"api error: {str(e)}".lower()