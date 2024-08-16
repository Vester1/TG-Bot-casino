import asyncio

from aiogram import Router, F
from aiogram.filters.callback_data import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from lexicon_ru import L_RU
from utilities.utilities import BETS, BASK_COMB
from keyboards.base_keyboards import get_kb_main_menu, get_kb_bet, get_kb_play_again


router = Router()
L_RU_cas = L_RU['casino']


@router.callback_query(F.data == '🏀')
async def choose_basketball(callback: CallbackQuery, balance: list[int]):
    await callback.answer()
    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass
    msg = await callback.message.answer_dice(emoji='🏀')
    hid_num = msg.dice.value
    bet = BETS[callback.from_user.id]
    print(balance)
    await asyncio.sleep(3.5)
    balance[0] -= bet
    balance[0] += round(bet * BASK_COMB[hid_num])
    rep_text = f"{L_RU_cas[f'bask_{hid_num}']}\n{L_RU_cas['balance'].format(balance[0])}"
    await callback.message.answer(rep_text, reply_markup=get_kb_main_menu())
    print(balance)
    await callback.message.answer(L_RU_cas['play_again'], reply_markup=get_kb_play_again('🏀'))


@router.callback_query(F.data == 'again🏀')
async def callback_play_again_basket(callback: CallbackQuery, balance: list[int]):
    await callback.answer()
    await callback.message.delete()
    if BETS[callback.from_user.id] > balance[0]:
        await callback.message.answer(L_RU_cas['not_engh_m'] + L_RU_cas['bet_balance']
                                      .format(balance[0], BETS[callback.from_user.id]), reply_markup=get_kb_bet())
    else:
        await choose_basketball(callback, balance)
