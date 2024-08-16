from aiogram.types import Message, BotCommand
from keyboards.base_keyboards import get_kb_bet
from aiogram import Bot

from lexicon_ru import L_RU

BETS = {}
PREV_BETS = {}


DICE_COMB = {
    '1-2': ([1, 2], 3),
    '3-4': ([3, 4], 3),
    '5-6': ([5, 6], 3),
    'even': ([2, 4, 6], 2),
    'odd': ([1, 3, 5], 2),
    '1': ([1], 6), '2': ([2], 6), '3': ([3], 6),
    '4': ([4], 6), '5': ([5], 6), '6': ([6], 6),
}

BASK_COMB = {
    1: 0,
    2: 0.3,
    3: 0.7,
    4: 1.5,
    5: 2,
}


async def update_bet_text(message: Message, new_value: int, balance: int):
    await message.edit_text(L_RU['casino']['bet_balance'].format(balance, new_value),
                            reply_markup=get_kb_bet())


async def set_main_menu(bot: Bot):
    commands = [BotCommand(
        command=c, description=d) for c, d in L_RU['menu_com'].items()
    ]
    await bot.set_my_commands(commands)
