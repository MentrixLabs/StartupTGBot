import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config import settings
from bot.api_client import APIClient
from bot.handlers import (
    start, look_goods, parsing, help, profile,
    delete_last_message, report, seo_and_ig, auth_handlers
)

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Глобально храним клиент и токены пользователей
    dp["api_client"] = APIClient()  # без токена – будет добавляться в каждом хендлере через state

    dp.include_routers(
        start.router,
        parsing.router,
        look_goods.router,
        help.router,
        profile.router,
        delete_last_message.router,
        report.router,
        seo_and_ig.router,
        auth_handlers.router
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass