import asyncio

from aiogram import Router, F
from aiogram.filters.callback_data import CallbackQuery
from psycopg import AsyncConnection

from lexicon_ru import L_RU
from utilities.utilities import DICE_COMB, ID_IN_PROGRESS
from keyboards.dice_keyboards import get_kb_guess_number, DiceNumCallbackData
from keyboards.base_keyboards import get_kb_main_menu, get_kb_choose_game, get_kb_play_again

from infrastructure.database.db import get_balance_and_bet, update_balance


L_RU_cas = L_RU['casino']
router = Router()


@router.callback_query(F.data.in_(['dice', 'again_dice']))
async def choose_dice(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(L_RU_cas['guess_n_st'], reply_markup=get_kb_guess_number())


@router.callback_query(DiceNumCallbackData.filter(F.value == '-1'))
async def callback_cancel_dice(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(L_RU_cas['choose_game'], reply_markup=get_kb_choose_game())


@router.callback_query(DiceNumCallbackData.filter())
async def callback_dice(callback: CallbackQuery, callback_data: DiceNumCallbackData, conn: AsyncConnection):
    await callback.answer()
    await callback.message.delete()

    ID_IN_PROGRESS.add(callback.from_user.id)
    balance, bet = await get_balance_and_bet(conn, user_id=callback.from_user.id)

    balance -= bet
    await update_balance(conn, user_id=callback.from_user.id, new_bal=balance)

    msg = await callback.message.answer_dice(emoji='🎲')
    hid_num = msg.dice.value

    await asyncio.sleep(3.5)

    chosen_value = callback_data.value
    chosen_nums = DICE_COMB[chosen_value][0]

    if hid_num not in chosen_nums:
        await callback.message.answer(f"{L_RU_cas['guess_n_lose']}\n"
                                      f"{L_RU_cas['balance'].format(balance)}",
                                      reply_markup=get_kb_main_menu())
    else:
        koef = DICE_COMB[chosen_value][1]
        won_prize = koef * bet
        balance += won_prize
        await update_balance(conn, user_id=callback.from_user.id, new_bal=balance)

        await callback.message.answer(f"{L_RU_cas['guess_n_win'].format(won_prize)}\n"
                                      f"{L_RU_cas['balance'].format(balance)}",
                                      reply_markup=get_kb_main_menu())

    await callback.message.answer(L_RU_cas['play_again'], reply_markup=get_kb_play_again('dice'))
    ID_IN_PROGRESS.discard(callback.from_user.id)

