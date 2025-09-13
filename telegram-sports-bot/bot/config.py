from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass
class Settings:
    telegram_token: str
    db_url: str
    admin_user_ids: list[int]


def load_settings() -> Settings:
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)

    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in .env")

    db_url = os.getenv("DATABASE_URL", "sqlite+pysqlite:///data/bot.sqlite3")
    admin_ids_raw = os.getenv("ADMIN_USER_IDS", "")
    admin_user_ids = [int(x) for x in admin_ids_raw.split(",") if x.strip().isdigit()]

    return Settings(
        telegram_token=token,
        db_url=db_url,
        admin_user_ids=admin_user_ids,
    )

