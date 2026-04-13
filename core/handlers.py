import os
import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from services.transcriber import transcribe_audio

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    # welcome message
    await message.answer("send voice or video note. i'll handle the rest.")


@router.message(F.voice | F.video_note)
async def handle_audio_content(message: Message, bot: Bot):
    # initial status
    status_msg = await message.answer("processing...")

    file_id = message.voice.file_id if message.voice else message.video_note.file_id
    file_info = await bot.get_file(file_id)
    ogg_path = f"temp/{file_id}.ogg"

    try:
        # downloading file
        await bot.download_file(file_info.file_path, destination=ogg_path)

        # running transcription in a separate thread
        transcribed_text = await asyncio.to_thread(transcribe_audio, ogg_path)

        await status_msg.edit_text(transcribed_text)

    except Exception as e:
        print(f"error: {e}")
        await status_msg.edit_text("failed to process.")

    finally:
        # cleanup
        if os.path.exists(ogg_path):
            os.remove(ogg_path)