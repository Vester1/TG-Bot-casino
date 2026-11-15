import logging

from aiogram import Router, F
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Message
from psycopg import AsyncConnection

from utilities.utilities import update_bet_text
from keyboards.base_keyboards import get_kb_main_menu, get_kb_bet, get_kb_choose_game, BetCallbackData
from lexicon_ru import L_RU
from infrastructure.database.db import update_balance, update_bet, get_balance, get_balance_and_bet

router = Router()
logger = logging.getLogger(__name__)
L_RU_cas = L_RU['casino']


@router.message(F.text == '\\')
async def bla(message: Message):
    msg = await message.answer_dice(emoji='🎰')
    await message.answer(text=f'{msg.dice.value}')


@router.message(F.text == '💸Пополнить баланс💸')
async def earn_money_handler(message: Message, conn: AsyncConnection):
    balance = await get_balance(conn, user_id=message.from_user.id)
    await update_balance(conn, user_id=message.from_user.id, new_bal=balance+100)
    logger.info("Got balance")
    await message.answer(L_RU_cas['earn_money'], reply_markup=get_kb_main_menu())


@router.message(F.text == '💰Изменить ставку💰')
async def change_bet_handler(message: Message, conn: AsyncConnection):
    balance, bet = await get_balance_and_bet(conn, user_id=message.from_user.id)
    await message.answer(L_RU_cas['bet_balance'].format(balance, bet),
                         reply_markup=get_kb_bet())


@router.message(F.text == '🎰Выбор режима🎰')
async def choose_game_handler(message: Message, conn: AsyncConnection):
    balance, bet = await get_balance_and_bet(conn, user_id=message.from_user.id)

    if bet == 0:
        await message.answer(f"{L_RU_cas['make_1st_bet']}\n{L_RU_cas['bet_balance'].format(balance, 0)}",
                             reply_markup=get_kb_bet())
    elif bet > balance:
        await message.answer(L_RU_cas['not_engh_m'] + L_RU_cas['bet_balance']
                             .format(balance, bet), reply_markup=get_kb_bet())
    else:
        await message.answer(L_RU_cas['choose_game'], reply_markup=get_kb_choose_game())


@router.callback_query(F.data == 'cg_cancel')
async def cancel_choose_game(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(L_RU['commands']['menu'], reply_markup=get_kb_main_menu())


@router.callback_query(BetCallbackData.filter(F.action == 'change'))
async def callback_change_bet(callback: CallbackQuery, callback_data: BetCallbackData, conn: AsyncConnection):
    balance, bet = await get_balance_and_bet(conn, user_id=callback.from_user.id)

    if bet + callback_data.bet_cng < 0:
        await callback.answer(L_RU_cas['er_less_zero'])
    else:
        new_bet = bet + callback_data.bet_cng
        await update_bet(conn, user_id=callback.from_user.id, new_bet=new_bet)
        await update_bet_text(callback.message, new_bet, balance)
    await callback.answer()


@router.callback_query(BetCallbackData.filter(F.action == 'finish'))
async def callback_confirm_bet(callback: CallbackQuery, conn: AsyncConnection):
    balance, bet = await get_balance_and_bet(conn, user_id=callback.from_user.id)
    
    if bet == 0:
        await callback.answer(L_RU_cas['er_zero'])
    elif bet > balance:
        await callback.answer(f"{L_RU_cas['er_not_enough_m']}\n")
    else:
        await callback.message.delete()
        await callback.message.answer(L_RU_cas['bet'].format(bet))
        await callback.message.answer(L_RU_cas['choose_game'], reply_markup=get_kb_choose_game())
    await callback.answer()


@router.callback_query(BetCallbackData.filter(F.action == 'cancel'))
async def callback_cancel_bet(callback: CallbackQuery, conn: AsyncConnection):
    await update_bet(conn, user_id=callback.from_user.id, new_bet=0)
    await callback.message.delete()
    await callback.message.answer(text=L_RU['commands']['menu'],
                                  reply_markup=get_kb_main_menu())
    await callback.answer()


@router.callback_query(F.data == 'choose_game_menu')
async def back_to_choose_game_menu(callback: CallbackQuery, conn: AsyncConnection):
    balance, bet = await get_balance_and_bet(conn, user_id=callback.from_user.id)

    await callback.answer()
    await callback.message.delete()
    if bet == 0:
        await callback.message.answer(f"{L_RU_cas['make_1st_bet']}\n{L_RU_cas['bet_balance'].format(balance, 0)}",
                                      reply_markup=get_kb_bet())
    elif bet > balance:
        await callback.message.answer(L_RU_cas['not_engh_m'] + L_RU_cas['bet_balance']
                  .format(balance, bet), reply_markup=get_kb_bet())
    else:
        await callback.message.answer(L_RU_cas['choose_game'], reply_markup=get_kb_choose_game())
