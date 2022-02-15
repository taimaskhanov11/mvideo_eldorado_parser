from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

btn_yes = KeyboardButton("Да")
btn_no = KeyboardButton("Нет")
choice_keyboard = ReplyKeyboardMarkup([[btn_yes, btn_no]], resize_keyboard=True)


btn_current_product = InlineKeyboardButton(
    text="Текущие товары", callback_data="current_products"
)
btn_add_product = InlineKeyboardButton(
    text="Добавить товары", callback_data="add_products"
)
btn_del_product = InlineKeyboardButton(
    text="Удалить товары", callback_data="del_products"
)
btn_clean_products = InlineKeyboardButton(
    text="Очистить все товары", callback_data="clean_products"
)

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [btn_current_product, btn_add_product],
        [btn_del_product, btn_clean_products],
    ]
)
