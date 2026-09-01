import asyncio

from aiogram import Router, F
from aiogram.filters.callback_data import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from lexicon_ru import L_RU
from utilities.utilities import BETS, SOCCER_COMB
from keyboards.base_keyboards import get_kb_main_menu, get_kb_play_again, get_kb_bet


router = Router()
L_RU_cas = L_RU['casino']


@router.callback_query(F.data == '⚽')
async def choose_soccer(callback: CallbackQuery, balance: list[int]):
    await callback.answer()
    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass
    msg = await callback.message.answer_dice(emoji='⚽')
    hid_num = msg.dice.value
    bet = BETS[callback.from_user.id]
    print(balance)
    await asyncio.sleep(3.5)
    balance[0] -= bet
    balance[0] += round(bet * SOCCER_COMB[hid_num])
    rep_text = f"{L_RU_cas[f'soc_{hid_num}']}\n{L_RU_cas['balance'].format(balance[0])}"
    await callback.message.answer(rep_text, reply_markup=get_kb_main_menu())
    print(balance)
    await callback.message.answer(L_RU_cas['play_again'], reply_markup=get_kb_play_again('⚽'))


@router.callback_query(F.data == 'again⚽')
async def callback_play_again_basket(callback: CallbackQuery, balance: list[int]):
    await callback.answer()
    await callback.message.delete()
    if BETS[callback.from_user.id] > balance[0]:
        await callback.message.answer(L_RU_cas['not_engh_m'] + L_RU_cas['bet_balance']
                                      .format(balance[0], BETS[callback.from_user.id]), reply_markup=get_kb_bet())
    else:
        await choose_soccer(callback, balance)
