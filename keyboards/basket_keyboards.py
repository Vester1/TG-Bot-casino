from lexicon_ru import L_RU

from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup


L_RU_kb = L_RU['kb']


def get_kb_play_again_basket():
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(callback_data='again🏀', text=L_RU_kb['pl_again'])]])
    return kb
