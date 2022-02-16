from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from mvideo_eldorado_parser.api.eldorado_api import ELDORADO_API
from mvideo_eldorado_parser.api.mvideo_api import MVIDEO_API

btn_yes = KeyboardButton("Да")
btn_no = KeyboardButton("Нет")
choice_keyboard = ReplyKeyboardMarkup([[btn_yes, btn_no]], resize_keyboard=True)

btn_mvideo = KeyboardButton("Mvideo")
btn_eldorado = KeyboardButton("Eldorado")
choice_store = ReplyKeyboardMarkup([[btn_mvideo, btn_eldorado]], resize_keyboard=True)


def get_stores_status():
    mvideo_button = InlineKeyboardButton(
        text="Приостановить Mvideo" if MVIDEO_API.launch_status else "Запуск Mvideo",
        callback_data="mvideo_launch"
    )
    eldorado_button = InlineKeyboardButton(
        text="Приостановить Eldorado" if MVIDEO_API.launch_status else "Запуск Eldorado",
        callback_data="eldorado_launch"
    )

    return mvideo_button, eldorado_button


btn_current_product_m = InlineKeyboardButton( #todo 16.02.2022 22:49 taima: укоротить
    text="Текущие товары Mvideo", callback_data="current_products_mvideo"
)
btn_add_product_m = InlineKeyboardButton(
    text="Добавить товары Mvideo", callback_data="add_products_mvideo"
)
btn_del_product_m = InlineKeyboardButton(
    text="Удалить товары Mvideo", callback_data="del_products_mvideo"
)
btn_clean_products_m = InlineKeyboardButton(
    text="Очистить все товары Mvideo", callback_data="clean_products_mvideo"
)

btn_current_product_e = InlineKeyboardButton(
    text="Текущие товары Eldorado", callback_data="current_products_eldorado"
)
btn_add_product_e = InlineKeyboardButton(
    text="Добавить товары Eldorado", callback_data="add_products_eldorado"
)
btn_del_product_e = InlineKeyboardButton(
    text="Удалить товары Eldorado", callback_data="del_products_eldorado"
)
btn_clean_products_e = InlineKeyboardButton(
    text="Очистить все товары Eldorado", callback_data="clean_products_eldorado"
)

main_menu_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [btn_current_product_m, btn_current_product_e],
        [btn_add_product_m, btn_add_product_e],
        [btn_del_product_m, btn_del_product_e],
        [btn_clean_products_m, btn_clean_products_e],
        [*get_stores_status()],

    ]
)
