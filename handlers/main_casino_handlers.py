from aiogram import Router, F
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Message

from utilities.utilities import update_bet_text, BETS, PREV_BETS
from keyboards.base_keyboards import get_kb_main_menu, get_kb_bet, get_kb_choose_game, BetCallbackData
from lexicon_ru import L_RU

router = Router()
L_RU_cas = L_RU['casino']


@router.message(F.dice)
async def bla(message: Message):
    print(message.dice.value)


@router.message(F.text == '💸Пополнить баланс💸')
async def earn_money_handler(message: Message, balance: list[int]):
    balance[0] += 100
    await message.answer(L_RU_cas['earn_money'], reply_markup=get_kb_main_menu())


@router.message(F.text == '💰Изменить ставку💰')
async def change_bet_handler(message: Message, balance: list[int]):
    BETS[message.from_user.id] = BETS.get(message.from_user.id, 0)
    await message.answer(L_RU_cas['bet_balance'].format(balance[0], BETS[message.from_user.id]),
                         reply_markup=get_kb_bet())


@router.message(F.text == '🎰Выбор режима🎰')
async def choose_game_handler(message: Message, balance: list[int]):
    if not BETS.get(message.from_user.id, 0):
        await message.answer(f"{L_RU_cas['make_1st_bet']}\n{L_RU_cas['bet_balance'].format(balance[0], 0)}",
                             reply_markup=get_kb_bet())
    elif BETS[message.from_user.id] > balance[0]:
        await message.answer(L_RU_cas['not_engh_m'] + L_RU_cas['bet_balance']
                             .format(balance[0], BETS[message.from_user.id]), reply_markup=get_kb_bet())
    else:
        await message.answer(L_RU_cas['choose_game'], reply_markup=get_kb_choose_game())


@router.callback_query(F.data == 'cg_cancel')
async def cancel_choose_game(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(L_RU['commands']['menu'], reply_markup=get_kb_main_menu())


@router.callback_query(BetCallbackData.filter(F.action == 'change'))
async def callback_change_bet(callback: CallbackQuery, callback_data: BetCallbackData, balance: list[int]):
    user_value = BETS.get(callback.from_user.id, 0)
    if user_value + callback_data.bet_cng < 0:
        await callback.answer(L_RU_cas['er_less_zero'])
    else:
        BETS[callback.from_user.id] = user_value + callback_data.bet_cng
        await update_bet_text(callback.message, BETS[callback.from_user.id], balance[0])
    await callback.answer()


@router.callback_query(BetCallbackData.filter(F.action == 'finish'))
async def callback_confirm_bet(callback: CallbackQuery, balance: list[int]):
    user_value = BETS.get(callback.from_user.id, 0)
    if user_value == 0:
        await callback.answer(L_RU_cas['er_zero'])
    elif user_value > balance[0]:
        await callback.answer(f"{L_RU_cas['er_not_enough_m']}\n")
    else:
        PREV_BETS[callback.from_user.id] = user_value
        await callback.message.delete()
        await callback.message.answer(L_RU_cas['bet'].format(user_value))
        await callback.message.answer(L_RU_cas['choose_game'], reply_markup=get_kb_choose_game())
    await callback.answer()


@router.callback_query(BetCallbackData.filter(F.action == 'cancel'))
async def callback_cancel_bet(callback: CallbackQuery):
    PREV_BETS.setdefault(callback.from_user.id, 0)
    BETS[callback.from_user.id] = PREV_BETS.pop(callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer(text=L_RU['commands']['menu'],
                                  reply_markup=get_kb_main_menu())
    await callback.answer()
