import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, User, TelegramObject
from psycopg import AsyncConnection

from infrastructure.database.db import get_balance_and_bet
from keyboards.dice_keyboards import DiceNumCallbackData
from lexicon_ru import L_RU

logger = logging.getLogger(__name__)


class CheckBalance(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            callback: CallbackQuery,
            data: dict[str, Any],
    ) -> Any:
        conn: AsyncConnection = data.get("conn")
        if conn is None:
            logger.error("Database connection not found in middleware data.")
            raise RuntimeError("Missing database connection for shadow ban check.")


        balance, bet = await get_balance_and_bet(conn, user_id=callback.from_user.id)
        if callback.data == DiceNumCallbackData(value=str(-1)).pack():
            return await handler(callback, data)
        if balance < bet:
            await callback.answer(L_RU['casino']['er_not_enough_m'])
            return
        if bet == 0:
            await callback.answer(L_RU['casino']['er_zero'])
            return
        return await handler(callback, data)

