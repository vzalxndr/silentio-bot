import os
import asyncio
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from services.transcriber import transcribe_audio, process_text_task
from core.config import INVITE_WORD

router = Router()

AUTHORIZED_USERS = set()


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
    if message.from_user.id in AUTHORIZED_USERS:
        await message.answer("Hi again. Send me a voice or video note.")
    else:
        await message.answer("Bot is locked. 🔒 Please enter the invite word.")


@router.message(F.text)
async def check_password(message: Message):
    user_id = message.from_user.id

    if user_id in AUTHORIZED_USERS:
        await message.answer("I only process voice and video notes. 🤫")
        return

    if message.text.strip() == INVITE_WORD:
        AUTHORIZED_USERS.add(user_id)
        await message.answer("Access granted! 🔓 You can now send voice and video notes.")
    else:
        await message.answer("Incorrect invite word.")


@router.message(F.voice | F.video_note)
async def handle_audio(message: Message, bot: Bot):
    if message.from_user.id not in AUTHORIZED_USERS:
        await message.answer("Bot is locked. 🔒 Please enter the invite word.")
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
    if callback.from_user.id not in AUTHORIZED_USERS:
        await callback.answer("Session expired. Please enter the invite word again.", show_alert=True)
        return

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