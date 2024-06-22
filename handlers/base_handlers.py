import random

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from keyboards.base_keyboards import get_keyboard_main_menu


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет, это казик, введи *\/menu* и начинай ~всасывать бабки~ играть')


@router.message(Command('menu'))
async def cmd_menu(message: Message):
    await message.answer('Выбирай, путник',
                         reply_markup=get_keyboard_main_menu())


@router.message(F.text.lower() == '👋🏿салам👋🏿')
async def salam_f(message: Message):
    await message.answer('*Salam, bradok*')


@router.message(F.text.lower() == '🤑заработать бабки🤑')
async def pls_babos(message: Message, balance: list[int]):
    balance[0] += 100
    await message.answer('Ок, \+100 к балику')


@router.message(F.text.lower() == '🤡крутые стики🤡')
async def prikol_sticks(message: Message, stickers: list[str]):
    await message.answer_sticker(random.Random().choice(stickers))


