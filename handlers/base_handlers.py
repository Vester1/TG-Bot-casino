from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from keyboards.base_keyboards import get_kb_main_menu
from lexicon_ru import L_RU


router = Router()
L_RU_cas = L_RU['commands']


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(L_RU_cas['start'])


@router.message(Command('menu'))
async def cmd_menu(message: Message):
    await message.answer(L_RU_cas['menu'],
                         reply_markup=get_kb_main_menu())


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(L_RU_cas['help'],
                         reply_markup=get_kb_main_menu())


@router.message(Command('info'))
async def cmd_info(message: Message):
    await message.answer(L_RU_cas['info'],
                         reply_markup=get_kb_main_menu())
