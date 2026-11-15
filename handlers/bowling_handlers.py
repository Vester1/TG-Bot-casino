import asyncio
import logging

from aiogram import Router, F
from aiogram.filters.callback_data import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from psycopg import AsyncConnection

from lexicon_ru import L_RU
from utilities.utilities import BOWLING_COMB, ID_IN_PROGRESS
from keyboards.base_keyboards import get_kb_main_menu, get_kb_play_again
from infrastructure.database.db import get_balance_and_bet, update_balance

router = Router()
logger = logging.getLogger(__name__)
L_RU_cas = L_RU['casino']


@router.callback_query(F.data.in_({'bowling', 'again_bowling'}))
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
    msg = await callback.message.answer_dice(emoji='🎳')
    hid_num: int = msg.dice.value
    await asyncio.sleep(3)

    balance += round(bet * BOWLING_COMB[hid_num])
    logger.info("balance: %s\ngot value: %s", balance, round(bet * BOWLING_COMB[hid_num]))
    await update_balance(conn, user_id=callback.from_user.id, new_bal=balance)

    rep_text = f"{L_RU_cas[f'bowling_{hid_num}']}\n{L_RU_cas['balance'].format(balance)}"
    await callback.message.answer(rep_text, reply_markup=get_kb_main_menu())
    await callback.message.answer(L_RU_cas['play_again'], reply_markup=get_kb_play_again('bowling'))

    ID_IN_PROGRESS.discard(callback.from_user.id)

