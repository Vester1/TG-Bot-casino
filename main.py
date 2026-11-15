import asyncio
import logging
import psycopg_pool

from aiogram.client.default import DefaultBotProperties
from config import Config, load_config
from aiogram import Bot, Dispatcher, Router
from aiogram.client.session.aiohttp import AiohttpSession

from handlers import (base_handlers, main_casino_handlers, dice_handlers,
                      basket_handlers, soccer_handlers, darts_hadlers, bowling_handlers, slot_handlers)

from middlewares import DataBaseMiddleware, AddUserDatabase, CheckGameInProgress, CheckBalance
from utilities.utilities import set_main_menu
from infrastructure.database.connection import get_pg_pool

# session = AiohttpSession(proxy='http://127.0.0.1:7897')
logger = logging.getLogger(__name__)
config: Config = load_config()

async def main():
    logging.basicConfig(level=logging.getLevelName(level=config.log.level),
                        format=config.log.format)

    bot = Bot(token=config.bot.token,
              default=DefaultBotProperties(parse_mode='HTML'),
              )
    dp = Dispatcher()
    logger.info("Starting bot")

    # Создаём пул соединений с Postgres
    db_pool: psycopg_pool.AsyncConnectionPool = await get_pg_pool(
        db_name=config.db.name,
        host=config.db.host,
        port=config.db.port,
        user=config.db.user,
        password=config.db.password,
    )

    game_router: Router = Router()
    game_router.include_routers(dice_handlers.router,
                                basket_handlers.router,
                                soccer_handlers.router,
                                darts_hadlers.router,
                                bowling_handlers.router,
                                slot_handlers.router,)
    dp.include_router(base_handlers.router)
    dp.include_router(main_casino_handlers.router)
    dp.include_router(game_router)


    dp.update.middleware(DataBaseMiddleware())
    dp.update.middleware(AddUserDatabase())
    dp.update.middleware(CheckGameInProgress())
    game_router.callback_query.middleware(CheckBalance())

    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(set_main_menu)

    # Запускаем поллинг
    try:
        await dp.start_polling(bot, db_pool=db_pool)
    except Exception as e:
        logger.exception(e)
    finally:
        # Закрываем пул соединений
        await db_pool.close()
        logger.info("Connection to Postgres closed")


if __name__ == "__main__":
    asyncio.run(main())
