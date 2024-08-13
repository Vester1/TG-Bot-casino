from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon_ru import L_RU


def get_kb_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=L_RU['kb']['mm_balance']),
        KeyboardButton(text=L_RU['kb']['mm_choice']),
        KeyboardButton(text=L_RU['kb']['mm_cng_bet'])
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
