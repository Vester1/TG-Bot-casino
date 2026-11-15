import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update, User, TelegramObject
from psycopg import AsyncConnection

from infrastructure.database.db import get_user, add_user

logger = logging.getLogger(__name__)


class AddUserDatabase(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")

        if user is None:
            return await handler(event, data)
        conn: AsyncConnection = data.get("conn")
        if conn is None:
            logger.error("Database connection not found in middleware data.")
            raise RuntimeError("Missing database connection for shadow ban check.")

        user_row = await get_user(conn, user_id=user.id)
        if user_row is None:
            logger.info("Adding user to database in %s.", __class__.__name__)
            await add_user(
                conn,
                user_id=user.id,
                username=user.username,
                language=user.language_code,
                balance=1000,
                bet=0,
            )
        return await handler(event, data)

