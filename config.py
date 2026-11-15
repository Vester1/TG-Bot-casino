import logging
import os
from dataclasses import dataclass

from environs import Env

logger = logging.getLogger(__name__)

@dataclass
class BotSettings:
    token: str

@dataclass
class DatabaseSettings:
    name: str
    host: str
    port: int
    user: str
    password: str

@dataclass
class LoggSettings:
    level: str
    format: str

@dataclass
class Config:
    bot: BotSettings
    db: DatabaseSettings
    log: LoggSettings


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    token = env("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN must not be empty")

    db = DatabaseSettings(
        name=env("POSTGRES_DB"),
        host=env("POSTGRES_HOST"),
        port=env.int("POSTGRES_PORT"),
        user=env("POSTGRES_USER"),
        password=env("POSTGRES_PASSWORD"),
    )

    logg_settings = LoggSettings(
        level=env("LOG_LEVEL"),
        format=env("LOG_FORMAT")
    )

    return Config(
        bot=BotSettings(token=token),
        db=db,
        log=logg_settings
    )