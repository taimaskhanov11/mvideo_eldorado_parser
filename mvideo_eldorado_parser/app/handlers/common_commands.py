from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from loguru import logger

from mvideo_eldorado_parser.api.eldorado_api import ELDORADO_API
from mvideo_eldorado_parser.api.mvideo_api import MVIDEO_API
from mvideo_eldorado_parser.app import markups
from mvideo_eldorado_parser.config.config import VERSION

STORES = {
    "Mvideo": MVIDEO_API,
    "Eldorado": ELDORADO_API
}


class TypeChoice(StatesGroup):
    run_stop_store = State()


async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f"Версия {VERSION}", reply_markup=markups.main_menu_inline())


async def run_stop_store_start(message: types.Message, state: FSMContext):
    logger.warning(message.text)
    answer = "Выберите магазин для запуска" if message.text == '/run' else "Выберите магазин для остановки"
    await message.answer(answer, reply_markup=markups.choice_store)
    await state.update_data(type=message.text)
    await TypeChoice.run_stop_store.set()


async def run_stop_store_end(message: types.Message, state: FSMContext):
    data = await state.get_data()
    store = STORES[message.text]
    choice_type = data["type"]
    if choice_type == '/run':
        if store.launch_status:
            await message.answer(f"{store} уже запущен")
        else:
            store.launch_status = False
            await message.answer(f"{store} будет приостановлен в течении 3-5 минут")
    else:
        if store.launch_status is False:
            await message.answer(f"{store} уже приостановлен")
        else:
            store.launch_status = False
            await message.answer(f"{store} будет запущен в течении 3-5 минут")


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start, commands="start", state="*")

    # dp.register_message_handler(run_stop_store_start, commands=["run", "stop"], state="*")
    # dp.register_message_handler(run_stop_store_end, state=TypeChoice.run_stop_store)

    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(
        cmd_cancel, Text(equals="отмена", ignore_case=True), state="*"
    )
