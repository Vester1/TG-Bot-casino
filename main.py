import asyncio
import logging
import random

from configs import config
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hide_link
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from typing import Optional
from aiogram.filters.callback_data import CallbackData


logging.basicConfig(level=logging.INFO)
anims = ['CgACAgQAAxkBAAIBGmWQMZuI4A3ZRC4dl7N76a5Z8AYYAAIkAwACBhcEU_zzWc930Hi_NAQ',
         'CgACAgQAAxkBAAIBG2WQMZsG_Be6X1VdBpXtawiz6yluAAI-AwACd1kFUzZ_JAi7KSw3NAQ',
         'CgACAgQAAxkBAAIBHGWQMZ4EicY5eZvwWHL-7FfkYvhpAAJDAwACgLoFUwJdqgTO1ShQNAQ',
         'CgACAgIAAxkBAAIBHmWQMaAKxpad-byyLf8JT01R7QyrAAKpGAACUFQBScrfAAEC2M66KDQE']
stickers = [
            'CAACAgIAAxkBAAICW2WRXat3Shp3fvBzXhOSyqeTEXJ3AAILAAMlUKUZJ0I9amwv-1A0BA',
            'CAACAgIAAxkBAAICXWWRXawrtzCMCXqiU424Cs0AAbUkqAACBgADJVClGXvbdXDWg3gQNAQ',
            'CAACAgIAAxkBAAICX2WRXa574pyEut2FqIIWcGD2J-mIAAIVAAMlUKUZf-Mqb9sL4_s0BA',
            'CAACAgIAAxkBAAICYWWRXbFx2rjntcRyOy-K839e1CA6AAJRAAMlUKUZmeS50x0o3fs0BA',
            'CAACAgIAAxkBAAICY2WRXbND7vV-7lNKdRU02vfULmFjAAJoAAMlUKUZKElkah7EMdQ0BA',
            'CAACAgIAAxkBAAICZWWRXbX-lngnQ8CWCreZcha19Jf5AAJ5AAMlUKUZInGTvhbMRgU0BA',
            'CAACAgIAAxkBAAICZ2WRXbYzPYwwSZt6Wn5kuB2TCyTIAAJ1AAMlUKUZcm9by53wzDw0BA',
            'CAACAgIAAxkBAAICaWWRXbjwz-jn0QRvCwyMKHPv7D7JAAKLAAMlUKUZxPevk94tTNU0BA',
            'CAACAgIAAxkBAAICa2WRXbm5BOKSVmcOsURojzdOVpf1AAKgAAMlUKUZcetTAdja41g0BA',
            'CAACAgIAAxkBAAICbWWRXboyXhMO49zCJVIzaYmMs5yTAAKWAAMlUKUZHwTRPdbgNLA0BA',
    ]
bets = {}

# Объект бота
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='MARKDOWNV2')
# Диспетчер
dp = Dispatcher()


def get_keyboard_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='👋🏿Салам👋🏿'),
        types.KeyboardButton(text='🎰Рулетка🎰')
    )
    builder.row(
        types.KeyboardButton(text='🤑Заработать бабки🤑'),
        types.KeyboardButton(text='🤡Крутые стики🤡')
    )
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_keyboard_bet():
    builder = InlineKeyboardBuilder()
    builder.button(text="➖10", callback_data=BetCallbackData(action='change', bet_cng=-10))
    builder.button(text="➖50", callback_data=BetCallbackData(action='change', bet_cng=-50))
    builder.button(text="➖250", callback_data=BetCallbackData(action='change', bet_cng=-250))
    builder.button(text="➖1000", callback_data=BetCallbackData(action='change', bet_cng=-1000))
    builder.button(text="Готово", callback_data=BetCallbackData(action='finish'))
    builder.button(text="➕10", callback_data=BetCallbackData(action='change', bet_cng=10))
    builder.button(text="➕50", callback_data=BetCallbackData(action='change', bet_cng=50))
    builder.button(text="➕250", callback_data=BetCallbackData(action='change', bet_cng=250))
    builder.button(text="➕1000", callback_data=BetCallbackData(action='change', bet_cng=1000))
    builder.adjust(4, 1, 4)
    return builder.as_markup()


def get_keyboard_guess_number():
    builder = InlineKeyboardBuilder()
    builder.button(text='1', callback_data=NumCallbackData(num=1))
    builder.button(text='2', callback_data=NumCallbackData(num=2))
    builder.button(text='3', callback_data=NumCallbackData(num=3))
    builder.button(text='4', callback_data=NumCallbackData(num=4))
    builder.button(text='5', callback_data=NumCallbackData(num=5))
    builder.button(text='6', callback_data=NumCallbackData(num=6))
    builder.adjust(2)
    return builder.as_markup()


@dp.message(Command("start"))
async def cmd_start(message: Message):
    print(message)
    await message.answer('Привет, это казик, введи *\/menu* и начинай ~всасывать бабки~ играть')


@dp.message(Command('menu'))
async def cmd_menu(message: Message):
    await message.answer('Выбирай, путник',
                         reply_markup=get_keyboard_main_menu())


@dp.message(F.text.lower() == '👋🏿салам👋🏿')
async def salam_f(message: Message):
    await message.answer(
        '*Salam, bradok*'
    )


class BetCallbackData(CallbackData, prefix='bet'):
    action: str
    bet_cng: Optional[int] = None


class NumCallbackData(CallbackData, prefix='num'):
    num: int


@dp.message(F.text.lower() == '🤑заработать бабки🤑')
async def pls_babos(message: Message, balance: list[int]):
    balance[0] += 100
    await message.answer('Ок, \+100 к балику')


@dp.message(F.text.lower() == '🤡крутые стики🤡')
async def prikol_sticks(message: Message, stickers: list[str]):
    await message.answer_sticker(random.Random().choice(stickers))


async def update_bet_text(message: types.Message, new_value: int):
    await message.edit_text(
        f"Ставка: {new_value}",
        reply_markup=get_keyboard_bet()
    )


@dp.message(F.text.lower() == '🎰рулетка🎰')
async def roulette(message: types.Message):
    bets[message.from_user.id] = bets.get(message.from_user.id, 0)
    await message.answer('💎*Сделайте ставку*💎')
    await message.answer(f"Ставка: {bets[message.from_user.id]}", reply_markup=get_keyboard_bet())


@dp.callback_query(BetCallbackData.filter(F.action == 'change'))
async def callback_change_bet(callback: types.CallbackQuery, callback_data: BetCallbackData):
    user_value = bets.get(callback.from_user.id, 0)
    if user_value + callback_data.bet_cng < 0:
        await callback.message.answer('❌*Ошибка*❌\nСтавка не может быть меньше нуля дебил')
    else:
        bets[callback.from_user.id] = user_value + callback_data.bet_cng
        await update_bet_text(callback.message, user_value + callback_data.bet_cng)
    await callback.answer()


@dp.callback_query(BetCallbackData.filter(F.action == 'finish'))
async def callback_change_bet(callback: types.CallbackQuery, balance: list[int]):
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


@dp.callback_query(NumCallbackData.filter())
async def callback_guess_number(callback: types.CallbackQuery, callback_data: NumCallbackData, balance: list[int]):
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


# Запуск процесса поллинга новых апдейтов
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, balance=[1000], anims=anims, stickers=stickers)


if __name__ == "__main__":
    asyncio.run(main())
