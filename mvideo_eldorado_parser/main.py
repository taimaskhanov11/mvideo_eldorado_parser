import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.types import BotCommand
from loguru import logger

from mvideo_eldorado_parser.api.eldorado_api import ELDORADO_API
from mvideo_eldorado_parser.api.mvideo_api import MVIDEO_API
from mvideo_eldorado_parser.app.bot import bot, dp
from mvideo_eldorado_parser.app.handlers.common_commands import \
    register_handlers_common
from mvideo_eldorado_parser.app.handlers.store_commands import \
    register_products_handlers
from mvideo_eldorado_parser.config.config import CONFIG

logger.remove()
logger.add(
    sink=sys.stdout,
    level=CONFIG["log_level"],
    enqueue=True,
    diagnose=True,
    # format="{time}| {message}",
)
logger.add(
    sink=f"../logs/mainlog.log",
    level="TRACE",
    enqueue=True,
    encoding="utf-8",
    diagnose=True,
)

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(filename="../logs/aiolog.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Init"),
        BotCommand(command="/cancel", description="Отменить текущее действие"),
        # BotCommand(command="/run", description="Запустить парсер"),
        # BotCommand(command="/stop", description="Остановить парсер"), #todo 16.02.2022 22:22 taima:
    ]
    await bot.set_my_commands(commands)


async def main():
    logger.error("Starting bot")
    logger.critical((await bot.get_me()).username)

    # Регистрация хэндлеров
    register_handlers_common(dp)
    register_products_handlers(dp)

    # Установка команд бота
    await set_commands(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)

    # Запуск парсеров цен
    asyncio.create_task(MVIDEO_API.start())
    asyncio.create_task(ELDORADO_API.start())

    await dp.skip_updates()
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
