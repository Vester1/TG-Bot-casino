import asyncio
import logging

from aiogram.client.default import DefaultBotProperties
from config import config
from aiogram import Bot, Dispatcher

from handlers import base_handlers, casino_handlers
from utilities.casino_utilities import anims, stickers


async def main():
    logging.basicConfig(level=logging.DEBUG)

    bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode='MarkdownV2'))
    dp = Dispatcher()

    dp.include_router(base_handlers.router)
    dp.include_router(casino_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, balance=[1000], anims=anims, stickers=stickers)


if __name__ == "__main__":
    asyncio.run(main())
