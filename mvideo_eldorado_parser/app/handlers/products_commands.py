import re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from mvideo_eldorado_parser.api.store_api import STORE_API
from mvideo_eldorado_parser.app.markups.main_markups import choice_keyboard


class ProductState(StatesGroup):
    add_products = State()
    del_products = State()
    clean_products = State()


async def get_current_products(call: types.CallbackQuery):
    product_ids = "\n".join(STORE_API.product_ids)
    await call.message.answer(product_ids)


async def add_products_start(call: types.CallbackQuery):
    await call.message.answer(
        "Введите коды товаров для добавления через запятую. Например:\n"
        "12341, 234523452, 73324523, 5672345238, 933453452"
    )
    await ProductState.add_products.set()


async def add_products_end(message: types.Message, state: FSMContext):
    product_ids = re.findall(r"(\d+),?\s?", message.text)
    STORE_API.add_products(product_ids)
    await message.answer("Товары успешно добавлены")
    await state.finish()


async def del_products_start(call: types.CallbackQuery):
    await call.message.answer(
        "Введите коды товаров для удаления через запятую. Например:\n"
        "12341, 234523452, 73324523, 5672345238, 933453452"
    )
    await ProductState.del_products.set()


async def del_products_end(message: types.Message, state: FSMContext):
    product_ids = re.findall(r"(\d+),?\s?", message.text)
    STORE_API.delete_products(product_ids)
    await message.answer(f"Товары {product_ids} успешно удалены")
    await state.finish()


async def clean_products_start(call: types.CallbackQuery):
    await call.message.answer("Вы уверены?", reply_markup=choice_keyboard)
    await ProductState.clean_products.set()


async def clean_products_end(message: types.Message, state: FSMContext):
    if message.text == "Да":
        STORE_API.clean_products()
        await message.answer("Список товаров очищен")
    else:
        await message.answer("Действие отменено")
        await state.finish()


def register_products_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(get_current_products, text="current_products")

    dp.register_callback_query_handler(add_products_start, text="add_products")
    dp.register_message_handler(add_products_end, state=ProductState.add_products)

    dp.register_callback_query_handler(del_products_start, text="del_products")
    dp.register_message_handler(del_products_end, state=ProductState.del_products)

    dp.register_callback_query_handler(clean_products_start, text="clean_products")
    dp.register_message_handler(clean_products_end, state=ProductState.clean_products)
