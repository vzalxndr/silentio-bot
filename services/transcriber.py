from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")


def transcribe_audio(file_path: str) -> str:
    try:
        segments, info = model.transcribe(file_path, beam_size=5)

        text = " ".join([segment.text for segment in segments])

        result = f"[detected: {info.language}] {text.strip()}".lower()

        if not text.strip():
            return "could not hear any voice."

        return result

    except Exception as e:
        return f"transcription error: {str(e)}".lower()