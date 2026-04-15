import os
import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from services.transcriber import transcribe_audio, process_text_task

router = Router()
MAX_DURATION = 120


def get_task_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Keep Raw", callback_data="task_raw")],
        [InlineKeyboardButton(text="Summary", callback_data="task_summary")],
        [InlineKeyboardButton(text="Make Note", callback_data="task_note")],
        [InlineKeyboardButton(text="AI Assistant", callback_data="task_assistant")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hi. Send or forward a voice/video note. I will transcribe it and ask what to do next.")

@router.message(F.voice | F.video_note)
async def handle_audio(message: Message, bot: Bot):
    duration = message.voice.duration if message.voice else message.video_note.duration

    if duration > MAX_DURATION:
        await message.answer(
            f"Audio is too long ({duration}s). Max allowed is 120 seconds."
        )
        return

    status_msg = await message.answer("Transcribing...")

    file_id = message.voice.file_id if message.voice else message.video_note.file_id
    file_info = await bot.get_file(file_id)
    
    ext = "ogg" if message.voice else "mp4"
    file_path = f"temp/{file_id}.{ext}"

    try:
        await bot.download_file(file_info.file_path, destination=file_path)
        
        text = await asyncio.to_thread(transcribe_audio, file_path)
        
        if "Error" in text or "Could not" in text:
            await status_msg.edit_text(text)
            return
        
        await status_msg.edit_text(
            f"Recognized text:\n\n{text}\n\nChoose an action:",
            reply_markup=get_task_keyboard()
        )

    except Exception as e:
        await status_msg.edit_text(f"Handler error: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@router.callback_query(F.data.startswith("task_"))
async def handle_task(callback: CallbackQuery):
    task = callback.data.split("_")[1]
    
    try:
        content = callback.message.text
        original_text = content.split("Recognized text:\n\n")[1].split("\n\nChoose an action:")[0]
    except Exception:
        await callback.answer("Could not parse text")
        return
    
    if task == "raw":
        await callback.message.edit_text(original_text)
        await callback.answer()
        return

    await callback.message.edit_text("Processing with AI...")

    result = await asyncio.to_thread(process_text_task, original_text, task)

    await callback.message.edit_text(result)
    await callback.answer()