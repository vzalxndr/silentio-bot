import os
import logging
from groq import Groq
from core.config import groq_api_key

client = Groq(api_key=groq_api_key)

SYSTEM_PROMPTS = {
    "base": (
        "You are a precise text processor. "
        "Never use emojis. ALWAYS respond in the exact same language as the user's input text."
    ),
    "summary": "Extract the core meaning and key details. Output only a concise summary. No introductory words.",
    "note": "Format the text into a structured, highly readable note using Markdown. Use bolding for key terms and bullet points. Keep it logical.",
    "assistant": "The user will dictate the context, meaning, or a rough draft of a message. Your task is to write a polished, natural, and polite chat message ready to be sent to someone based on this context. Fix any awkward phrasing. Output ONLY the final message text, with no introductory or concluding remarks."
}

def transcribe_audio(file_path: str) -> str:
    try:
        file_name = os.path.basename(file_path)
        
        with open(file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(file_name, file.read()),
                model="whisper-large-v3-turbo",
                response_format="verbose_json",
            )
        
        lang = transcription.language
        text = transcription.text
        
        if not text or not text.strip():
            return "Could not detect any speech."
            
        return f"[detected: {lang}] {text.strip()}"

    except Exception as e:
        logging.error(f"Whisper API error: {e}")
        return "Error: transcription failed."

def process_text_task(text: str, task: str) -> str:
    system_content = f"{SYSTEM_PROMPTS['base']} {SYSTEM_PROMPTS.get(task, 'Process the text.')}"
    temp = 0.7 if task == "assistant" else 0.3

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": text}
            ],
            temperature=temp,
        )
        
        return completion.choices[0].message.content.strip()
        
    except Exception as e:
        logging.error(f"Llama API error: {e}")
        return "Error: AI processing failed."