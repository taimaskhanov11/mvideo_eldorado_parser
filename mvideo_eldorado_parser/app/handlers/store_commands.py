import re

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from mvideo_eldorado_parser.api.eldorado_api import ELDORADO_API
from mvideo_eldorado_parser.api.mvideo_api import MVIDEO_API
from mvideo_eldorado_parser.app import markups
from mvideo_eldorado_parser.app.markups.main_markups import choice_keyboard
# todo 16.02.2022 23:00 taima: Почистить
from mvideo_eldorado_parser.config.config import VERSION


class ProductState(StatesGroup):
    add_products = State()
    del_products = State()
    clean_products = State()


STORES = {
    "mvideo": MVIDEO_API,
    "eldorado": ELDORADO_API
}

product_ids_pattern = re.compile(r"(\d+),?\s?")


async def get_current_products(call: types.CallbackQuery, ):
    store = STORES[re.findall(r"current_products_(.*)", call.data)[0]]
    product_ids = "\n".join(store.product_ids)
    await call.message.answer(product_ids)


async def add_products_start(call: types.CallbackQuery, state: FSMContext):
    store = re.findall(r"add_products_(.*)", call.data)[0]
    await state.update_data(store=store)
    await call.message.answer("Выберите парсер", reply_markup=markups.choice_store)
    await call.message.answer(
        "Введите коды товаров для добавления через запятую. Например:\n"
        "12341, 234523452, 73324523, 5672345238, 933453452"
    )
    await ProductState.add_products.set()


async def add_products_end(message: types.Message, state: FSMContext):
    data = await state.get_data()
    store = STORES[data["store"]]
    product_ids = re.findall(product_ids_pattern, message.text)
    store.add_products(product_ids)
    await message.answer("Товары успешно добавлены")
    await state.finish()


async def del_products_start(call: types.CallbackQuery, state: FSMContext):
    store = re.findall(r"del_products_(.*)", call.data)[0]
    await state.update_data(store=store)
    await call.message.answer(
        "Введите коды товаров для удаления через запятую. Например:\n"
        "12341, 234523452, 73324523, 5672345238, 933453452"
    )
    await ProductState.del_products.set()


async def del_products_end(message: types.Message, state: FSMContext):
    product_ids = re.findall(product_ids_pattern, message.text)
    data = await state.get_data()
    store = STORES[data["store"]]
    store.delete_products(product_ids)
    await message.answer(f"Товары {product_ids} успешно удалены")
    await state.finish()


async def clean_products_start(call: types.CallbackQuery, state: FSMContext):
    store = re.findall(r"clean_products_(.*)", call.data)[0]
    await state.update_data(store=store)

    await call.message.answer("Вы уверены?", reply_markup=choice_keyboard)
    await ProductState.clean_products.set()


async def clean_products_end(message: types.Message, state: FSMContext):
    data = await state.get_data()
    store = STORES[data["store"]]
    if message.text == "Да":
        store.clean_products()
        await message.answer("Список товаров очищен")
    else:
        await message.answer("Действие отменено")
    await state.finish()


async def store_launch(call: types.CallbackQuery):
    store = MVIDEO_API if call.data == "mvideo_launch" else ELDORADO_API
    if store.launch_status:
        store.launch_status = False
        await call.message.answer(f"{store}| Парсер будет выключен в течении 3-5 минут")

    else:
        store.launch_status = True
        await call.message.answer(f"{store}| Парсер будет запущен в течении 20-30 секунд")
    # await call.message.answer(f"Версия {VERSION}", reply_markup=markups.main_menu_inline())
    await call.message.edit_reply_markup(markups.main_menu_inline())


def register_products_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        get_current_products,
        # text="current_products"
        lambda call: call.data in ["current_products_mvideo", "current_products_eldorado"]

    )

    dp.register_callback_query_handler(
        store_launch,
        lambda call: call.data in ["mvideo_launch", "eldorado_launch"]
    )

    # dp.register_callback_query_handler(
    #     choice_store,
    #     lambda call: call.data in ["add_products", "del_products", "clean_products"]
    # )

    dp.register_callback_query_handler(
        add_products_start,
        # text="add_products",
        lambda call: call.data in ["add_products_mvideo", "add_products_eldorado"]
    )
    dp.register_message_handler(add_products_end, state=ProductState.add_products)

    dp.register_callback_query_handler(
        del_products_start,
        # text="del_products"
        lambda call: call.data in ["del_products_mvideo", "del_products_eldorado"]
    )
    dp.register_message_handler(del_products_end, state=ProductState.del_products)

    dp.register_callback_query_handler(
        clean_products_start,
        # text="clean_products"
        lambda call: call.data in ["clean_products_mvideo", "clean_products_eldorado"]
    )
    dp.register_message_handler(clean_products_end, state=ProductState.clean_products)
