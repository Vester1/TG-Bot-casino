import asyncio
import random

from aiogram import Router, F
from aiogram.filters.callback_data import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from psycopg import AsyncConnection

from lexicon_ru import L_RU
from utilities.utilities import SLOT_COMB, SLOT_SMILES, ID_IN_PROGRESS
from keyboards.base_keyboards import get_kb_main_menu, get_kb_play_again
from infrastructure.database.db import get_balance_and_bet, update_balance


router = Router()
L_RU_cas = L_RU['casino']


@router.callback_query(F.data.in_(['slot', 'again_slot']))
async def choose_basketball(callback: CallbackQuery, conn: AsyncConnection):
    await callback.answer()
    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass

    ID_IN_PROGRESS.add(callback.from_user.id)
    balance, bet = await get_balance_and_bet(conn, user_id=callback.from_user.id)

    balance -= bet
    await update_balance(conn, user_id=callback.from_user.id, new_bal=balance)

    msg = await callback.message.answer_dice(emoji='🎰')
    hid_num: int = msg.dice.value

    coef = 0
    suf = ''
    for x in SLOT_COMB:
        if hid_num in x:
            coef = SLOT_COMB[x]
            suf = x[-1]
            break
    won_prize: int = round(bet * coef)
    balance += won_prize
    await update_balance(conn, user_id=callback.from_user.id, new_bal=balance)

    await asyncio.sleep(1.7)

    if suf == '':
        rep_text = f"{L_RU_cas[f'slot_lose'].format(random.choice(SLOT_SMILES))}\n"
    elif suf[0] == '3':
        rep_text = f"{L_RU_cas[f'slot_{suf}'].format(bet, won_prize)}\n"
    else:
        rep_text = f"{L_RU_cas[f'slot_{suf}'].format(won_prize)}\n"

    rep_text += f"{L_RU_cas['balance'].format(balance)}"
    await callback.message.answer(rep_text, reply_markup=get_kb_main_menu())
    await callback.message.answer(L_RU_cas['play_again'], reply_markup=get_kb_play_again('slot'))

    ID_IN_PROGRESS.discard(callback.from_user.id)
