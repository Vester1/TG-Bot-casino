from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text='👋🏿Салам👋🏿'),
        KeyboardButton(text='🎰Рулетка🎰')
    )
    builder.row(
        KeyboardButton(text='🤑Заработать бабки🤑'),
        KeyboardButton(text='🤡Крутые стики🤡')
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
