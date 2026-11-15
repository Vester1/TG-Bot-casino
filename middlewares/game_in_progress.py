import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update, User

from utilities.utilities import ID_IN_PROGRESS
from lexicon_ru import L_RU

logger = logging.getLogger(__name__)


class CheckGameInProgress(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        user_id: int = user.id
        if user_id in ID_IN_PROGRESS:
            if event.message is not None:
                await event.message.answer(text=L_RU['casino']['wait'])
            elif event.callback_query is not None:
                await event.callback_query.answer(text=L_RU['casino']['wait'])
            return
        return await handler(event, data)
