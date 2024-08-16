from lexicon_ru import L_RU

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

L_RU_kb = L_RU['kb']


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
