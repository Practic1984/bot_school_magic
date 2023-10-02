from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BLOCK, GROUP_URL
def menu_main():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Ввести промокод", callback_data="promo"),
        InlineKeyboardButton(BLOCK, callback_data="block"),
    )

    return markup

def go_group():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("Перейти в группу", url=GROUP_URL),
        InlineKeyboardButton("Назад", callback_data='back'),
    )
    return markup