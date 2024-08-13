from typing import Optional

from lexicon_ru import L_RU

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

L_RU_kb = L_RU['kb']


class BetCallbackData(CallbackData, prefix='bet'):
    action: str
    bet_cng: Optional[int] = None


class DiceNumCallbackData(CallbackData, prefix='dice'):
    value: str


def get_kb_guess_number():
    builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(
        text=j, callback_data=DiceNumCallbackData(value=i).pack()) for i, j in L_RU_kb['dice'].items()]
    buttons += [InlineKeyboardButton(
        text=str(i), callback_data=DiceNumCallbackData(value=str(i)).pack()) for i in range(1, 7)]
    builder.row(*buttons)
    builder.add(*[InlineKeyboardButton(text=L_RU_kb['cancel'],
                                       callback_data=DiceNumCallbackData(value='-1').pack())])
    builder.adjust(3, 2, 6, 1)
    return builder.as_markup()


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


def get_kb_play_again():
    kb = InlineKeyboardMarkup(inline_keyboard=
                              [[InlineKeyboardButton(callback_data='again🎲', text=L_RU_kb['pl_again'])]]
                              )
    return kb
