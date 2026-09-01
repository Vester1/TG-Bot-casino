import asyncio
import logging

from aiogram.client.default import DefaultBotProperties
from config import config
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from handlers import (base_handlers, main_casino_handlers, dice_handlers,
                      basket_handlers, soccer_handlers, darts_hadlers, bowling_handlers, slot_handlers)
from utilities.utilities import set_main_menu

session = AiohttpSession(
    proxy="http://127.0.0.1:12334"
)
async def main():
    logging.basicConfig(level=logging.DEBUG)

    bot = Bot(token=config.bot_token.get_secret_value(),
              default=DefaultBotProperties(parse_mode='HTML'),
              session=session)
    dp = Dispatcher()

    dp.include_router(base_handlers.router)
    dp.include_router(main_casino_handlers.router)
    dp.include_router(dice_handlers.router)
    dp.include_router(basket_handlers.router)
    dp.include_router(soccer_handlers.router)
    dp.include_router(darts_hadlers.router)
    dp.include_router(bowling_handlers.router)
    dp.include_router(slot_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(set_main_menu)

    await dp.start_polling(bot, balance=[1000])

if __name__ == "__main__":
    asyncio.run(main())
