import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiohttp import web  # Добавили это
from core.config import bot_token
from core.handlers import router


# healthcheck handler
async def health_check(request):
    return web.Response(text="bot active.", status=200)


async def main():
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    dp.include_router(router)

    # web server settings
    app = web.Application()
    app.router.add_get("/", health_check)
    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.environ.get("PORT", 7860))
    site = web.TCPSite(runner, "0.0.0.0", port)

    await site.start()
    print(f"health check server started on port {port}")

    print("bot active.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("bot stopped.")