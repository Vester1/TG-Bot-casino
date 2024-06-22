import random

from aiogram import Router, F
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Message

from utilities.casino_utilities import update_bet_text
from keyboards.casino_keyboards import (get_keyboard_bet, get_keyboard_guess_number,
                                        BetCallbackData, NumCallbackData)
from keyboards.base_keyboards import get_keyboard_main_menu


router = Router()

bets = {}


@router.message(F.text.lower() == '🎰рулетка🎰')
async def roulette(message: Message):
    bets[message.from_user.id] = bets.get(message.from_user.id, 0)
    await message.answer('💎*Сделайте ставку*💎')
    await message.answer(f"Ставка: {bets[message.from_user.id]}", reply_markup=get_keyboard_bet())


@router.callback_query(BetCallbackData.filter(F.action == 'change'))
async def callback_change_bet(callback: CallbackQuery, callback_data: BetCallbackData):
    user_value = bets.get(callback.from_user.id, 0)
    if user_value + callback_data.bet_cng < 0:
        await callback.message.answer('❌*Ошибка*❌\nСтавка не может быть меньше нуля дебил')
    else:
        bets[callback.from_user.id] = user_value + callback_data.bet_cng
        await update_bet_text(callback.message, user_value + callback_data.bet_cng)
    await callback.answer()


@router.callback_query(BetCallbackData.filter(F.action == 'finish'))
async def callback_change_bet(callback: CallbackQuery, balance: list[int]):
    user_value = bets.get(callback.from_user.id, 0)
    if user_value == 0:
        await callback.message.answer('❌*Ошибка*❌\nСтавка не может быть равна нулю дебил')
    elif user_value > balance[0]:
        await callback.message.answer('❌*Ошибка*❌\nУ тебя слишком мало бабок дебил')
        await callback.message.answer(f'💎Баланс: {balance[0]}💎')
    else:
        await callback.message.delete()
        await callback.message.answer(f'💰Ставка: {user_value}💰')
        await callback.message.answer('Теперь, я загадываю число от 1 до 6\n'
                                      'Если угадаешь, получишь 🤑*x3 ставку*🤑',
                                      reply_markup=get_keyboard_guess_number())

    await callback.answer()


@router.callback_query(NumCallbackData.filter())
async def callback_guess_number(callback: CallbackQuery, callback_data: NumCallbackData, balance: list[int]):
    hid_num = random.Random().randint(1, 6)
    num = callback_data.num
    bet = bets[callback.from_user.id]
    if hid_num != num:
        balance[0] -= bet
        await callback.message.edit_text(f'~Ура~ 😓О но, ты слил😓\n'
                                         f'😡Ну ни че, ещё повезёт😡\n'
                                         f'💎Баланс: {balance[0]}💎')
    else:
        balance[0] += bet * 3
        await callback.message.edit_text(f'~О но~ 🤑ЕЕЕ, плюс бабки🤑\n'
                                         f'💰Изи {bet * 3} ~фантиков~ рубасов💰\n'
                                         f'🤭Щас на балике \- {balance[0]}🤭')
    await callback.message.answer('Выбирай, путник', reply_markup=get_keyboard_main_menu())
    await callback.answer()
