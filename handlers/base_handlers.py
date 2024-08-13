from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from keyboards.base_keyboards import get_kb_main_menu
from lexicon_ru import L_RU


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(L_RU['commands']['start'])


@router.message(Command('menu'))
async def cmd_menu(message: Message):
    await message.answer(L_RU['commands']['menu'],
                         reply_markup=get_kb_main_menu())


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(L_RU['commands']['help'],
                         reply_markup=get_kb_main_menu())


@router.message(Command('info'))
async def cmd_help(message: Message):
    await message.answer(L_RU['commands']['info'],
                         reply_markup=get_kb_main_menu())
