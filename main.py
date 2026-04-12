import asyncio
import logging
from aiogram import Bot, Dispatcher
from core.config import bot_token
from core.handlers import router

async def main():
    bot = Bot(token=bot_token)
    dp = Dispatcher()

    dp.include_router(router)

    print("bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())