import os
import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters import Command
from services.transcriber import transcribe_audio

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("hi. send me a voice message and i will auto-detect the language and transcribe it.")


@router.message(F.voice)
async def handle_voice(message: Message, bot: Bot):
    status_msg = await message.answer("processing your voice with ai...")

    voice_id = message.voice.file_id
    file_info = await bot.get_file(voice_id)

    ogg_path = f"temp/{voice_id}.ogg"

    try:
        await bot.download_file(file_info.file_path, destination=ogg_path)

        transcribed_text = await asyncio.to_thread(transcribe_audio, ogg_path)

        await status_msg.edit_text(transcribed_text)

    except Exception as e:
        error_text = f"an error occurred: {str(e)}".lower()
        await status_msg.edit_text(error_text)

    finally:
        if os.path.exists(ogg_path):
            os.remove(ogg_path)