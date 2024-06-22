from dataclasses import dataclass
from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class BetCallbackData(CallbackData, prefix='bet'):
    action: str
    bet_cng: Optional[int] = None


class NumCallbackData(CallbackData, prefix='num'):
    num: int


def get_keyboard_guess_number():
    builder = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=f'{i}', callback_data=NumCallbackData(num=i).pack()) for i in range(1, 7)]
    builder.row(*buttons)
    builder.adjust(2)
    return builder.as_markup()


def get_keyboard_bet():
    builder = InlineKeyboardBuilder()
    builder.add(*[InlineKeyboardButton(
        text=f'➖{abs(i)}', callback_data=BetCallbackData(action='change', bet_cng=i).pack()
    ) for i in [-10, -50, -250, -1000]])
    builder.button(text="Готово", callback_data=BetCallbackData(action='finish'))
    builder.add(*[InlineKeyboardButton(
        text=f'➕{i}', callback_data=BetCallbackData(action='change', bet_cng=i).pack()
    ) for i in [10, 50, 250, 1000]])
    builder.adjust(4, 1, 4)
    return builder.as_markup()
