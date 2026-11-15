import logging
from datetime import datetime, timezone
from typing import Any, Tuple

from psycopg import AsyncConnection

logger = logging.getLogger(__name__)


async def add_user(
    conn: AsyncConnection,
    *,
    user_id: int,
    username: str | None = None,
    language: str = "ru",
    balance: int = 0,
    bet: int = 0,
) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="""
                INSERT INTO users(user_id, username, language, balance, bet)
                VALUES(
                    %(user_id)s, 
                    %(username)s, 
                    %(language)s, 
                    %(balance)s, 
                    %(bet)s
                ) ON CONFLICT DO NOTHING;
            """,
            params={
                "user_id": user_id,
                "username": username,
                "language": language,
                "balance": balance,
                "bet": bet,
            },
        )
    logger.info(
        "User added. Table=`%s`, user_id=%d, created_at='%s', "
        "language='%s', balance=%s, bet=%s",
        "users",
        user_id,
        datetime.now(timezone.utc),
        language,
        balance,
        bet,
    )


async def get_user(
    conn: AsyncConnection,
    *,
    user_id: int,
) -> tuple[Any, ...] | None:
    async with conn.cursor() as cursor:
        data = await cursor.execute(
            query="""
                SELECT 
                    id,
                    user_id,
                    username,
                    created_at,
                    language,
                    balance,
                    bet
                    FROM users WHERE user_id = %s;
            """,
            params=(user_id,),
        )
        row = await data.fetchone()
    return row if row else None


async def update_balance(
    conn: AsyncConnection,
    *,
    user_id: int,
    new_bal: int,
) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="""
            UPDATE users
            SET balance = %s
            WHERE user_id = %s;
            """,
            params=(new_bal, user_id),
        )
    logger.info("Balance of %s changed to %s", user_id, new_bal)


async def update_bet(
    conn: AsyncConnection,
    *,
    user_id: int,
    new_bet: int,
) -> None:
    async with conn.cursor() as cursor:
        await cursor.execute(
            query="""
            UPDATE users
            SET bet = %s
            WHERE user_id = %s;
            """,
            params=(new_bet, user_id),
        )
    logger.info("Bet of %s changed to %s", user_id, new_bet)


async def get_balance(
    conn: AsyncConnection,
    *,
    user_id: int,
) -> int:
    async with conn.cursor() as cursor:
        data = await cursor.execute(
            query="""
            SELECT balance
            FROM users WHERE user_id = %s;
            """,
            params=(user_id,),
        )
        row = await data.fetchone()
        balance = int(row[0])
    logger.info("Got balance of %s: %s", user_id, balance)
    return balance


async def get_bet(
    conn: AsyncConnection,
    *,
    user_id: int,
) -> int:
    async with conn.cursor() as cursor:
        data = await cursor.execute(
            query="""
            SELECT bet
            FROM users WHERE user_id = %s;
            """,
            params=(user_id,),
        )
        row = await data.fetchone()
        bet = int(row[0])
    logger.info("Got bet of %s: %s", user_id, bet)
    return bet


async def get_balance_and_bet(
    conn: AsyncConnection,
    *,
    user_id: int,
) -> Tuple[int]:
    async with conn.cursor() as cursor:
        data = await cursor.execute(
            query="""
            SELECT balance, bet 
            FROM users WHERE user_id = %s;
            """,
            params=(user_id,),
        )
        row = await data.fetchone()
        row = tuple(row)
    logger.info("Got balance and bet of %s: %s", user_id, row)
    return row