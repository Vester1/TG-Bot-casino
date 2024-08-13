import asyncio

from aiogram import Router, F
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Message

from lexicon_ru import L_RU
from utilities.utilities import BETS, PREV_BETS, DICE_COMB
from keyboards.casino_keyboards import (get_kb_guess_number, DiceNumCallbackData,
                                        get_kb_choose_game, get_kb_play_again, get_kb_bet)
from keyboards.base_keyboards import get_kb_main_menu


L_RU_cas = L_RU['casino']
router = Router()


@router.callback_query(F.data.in_(['🎰', '🎲', '🎯', '🎳', '🏀', '⚽']))
async def roulette(callback: CallbackQuery):
    await callback.message.delete()
    if callback.data == '🎲':
        await callback.message.answer(L_RU_cas['guess_n_st'], reply_markup=get_kb_guess_number())
    else:
        await callback.message.answer('В разработке')
    await callback.answer()


@router.callback_query(DiceNumCallbackData.filter(F.value == '-1'))
async def callback_cancel_dice(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(L_RU_cas['choose_game'], reply_markup=get_kb_choose_game())


@router.callback_query(DiceNumCallbackData.filter())
async def callback_dice(callback: CallbackQuery, callback_data: DiceNumCallbackData, balance: list[int]):
    await callback.answer()
    await callback.message.delete()
    msg = await callback.message.answer_dice(emoji='🎲')
    await asyncio.sleep(3.5)
    val = callback_data.value
    num = DICE_COMB[val][0]
    hid_num = msg.dice.value
    bet = BETS[callback.from_user.id]
    if hid_num not in num:
        balance[0] -= bet
        await callback.message.answer(f"{L_RU_cas['guess_n_lose']}\n"
                                      f"{L_RU_cas['balance'].format(balance[0])}",
                                      reply_markup=get_kb_main_menu())
    else:
        mult = DICE_COMB[val][1]
        prize = round(bet * mult)
        balance[0] += prize
        await callback.message.answer(f"{L_RU_cas['guess_n_win'].format(prize)}\n"
                                      f"{L_RU_cas['balance'].format(balance[0])}",
                                      reply_markup=get_kb_main_menu())

    await callback.message.answer(L_RU_cas['play_again'], reply_markup=get_kb_play_again())


@router.callback_query(F.data == 'again🎲')
async def callback_play_again_dice(callback: CallbackQuery, balance: list[int]):
    await callback.answer()
    await callback.message.delete()
    if BETS[callback.from_user.id] > balance[0]:
        await callback.message.answer(L_RU_cas['not_engh_m'] + L_RU_cas['bet_balance']
                             .format(balance[0], BETS[callback.from_user.id]), reply_markup=get_kb_bet())
    else:
        await callback.message.answer(L_RU_cas['guess_n_st'], reply_markup=get_kb_guess_number())

