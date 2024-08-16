from typing import Optional

from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from lexicon_ru import L_RU


L_RU_kb = L_RU['kb']


class BetCallbackData(CallbackData, prefix='bet'):
    action: str
    bet_cng: Optional[int] = None


def get_kb_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=L_RU['kb']['mm_balance']),
        KeyboardButton(text=L_RU['kb']['mm_choice']),
        KeyboardButton(text=L_RU['kb']['mm_cng_bet'])
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_kb_bet():
    builder = InlineKeyboardBuilder()
    builder.add(*[InlineKeyboardButton(
        text=f'➖{i}', callback_data=BetCallbackData(action='change', bet_cng=-i).pack()
    ) for i in [10, 50, 250, 1000]])
    builder.button(text=L_RU_kb['ready'], callback_data=BetCallbackData(action='finish'))
    builder.button(text=L_RU_kb['cancel'], callback_data=BetCallbackData(action='cancel'))
    builder.add(*[InlineKeyboardButton(
        text=f'➕{i}', callback_data=BetCallbackData(action='change', bet_cng=i).pack()
    ) for i in [10, 50, 250, 1000]])
    builder.adjust(4, 2, 4)
    return builder.as_markup()


def get_kb_choose_game():
    builder = InlineKeyboardBuilder()
    builder.add(*[InlineKeyboardButton(text=j, callback_data=i) for i, j in L_RU_kb['games'].items()])
    builder.add(InlineKeyboardButton(text=L_RU_kb['cancel'], callback_data='cg_cancel'))
    builder.adjust(1, 2, 3, 1)
    return builder.as_markup()


def get_kb_play_again(emoji):
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(callback_data=f'again{emoji}',
                             text=f'{emoji}{L_RU_kb["pl_again"]}{emoji}')]])
    return kb
