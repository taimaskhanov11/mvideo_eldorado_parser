from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from mvideo_eldorado_parser.config.config import TG_TOKEN

# Объявление и инициализация объектов бота и диспетчера

bot = Bot(token=TG_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(
    bot,
    storage=MemoryStorage(),
)
