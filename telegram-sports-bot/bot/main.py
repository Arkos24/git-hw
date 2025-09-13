from __future__ import annotations

import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.config import load_settings
from bot.db import create_session_factory, session_scope
from bot.data_sources.stub import StubDataSource
from bot.models.predictors import EloRating
from bot.bankroll.strategies import recommend_stake


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот-прототип для спортивных прогнозов. Команды:\n"
        "/predict — показать прогнозы на ближайшие матчи (демо)\n"
        "/help — помощь"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "/predict — прогноз на ближайшие матчи (демо на заглушке).\n"
        "Для работы нужен токен бота в .env и запуск main.py."
    )


@router.message(Command("predict"))
async def cmd_predict(message: Message):
    data_source = StubDataSource()
    elo = EloRating()
    matches = [m async for m in _aiter(await data_source.fetch_upcoming_matches())]

    if not matches:
        await message.answer("Нет матчей в ближайшее время.")
        return

    lines: list[str] = []
    for m in matches:
        ph, pd, pa = elo.predict_win_prob(m.home_team, m.away_team)
        # простая ставка на фаворита по вероятности
        if ph >= pa and ph >= pd:
            selection = f"Победа {m.home_team}"
            prob = ph
            demo_odds = 1.9
        elif pa >= ph and pa >= pd:
            selection = f"Победа {m.away_team}"
            prob = pa
            demo_odds = 1.9
        else:
            selection = "Ничья"
            prob = pd
            demo_odds = 3.2

        stake = recommend_stake("kelly_half", bankroll=10000.0, prob=prob, odds=demo_odds)
        when = m.start_time.strftime("%Y-%m-%d %H:%M UTC")
        lines.append(
            f"{m.league}: {m.home_team} vs {m.away_team} — {when}\n"
            f"Выбор: {selection} | P≈{prob:.2f} | Кэф≈{demo_odds:.2f} | Ставка≈{stake:.0f}₽"
        )

    text = "\n\n".join(lines)
    await message.answer(text)


async def _aiter(iterable):
    for item in iterable:
        yield item


async def main():
    settings = load_settings()
    Session = create_session_factory(settings.db_url)
    # Ensure DB is reachable once
    with session_scope(Session) as _:
        pass

    bot = Bot(token=settings.telegram_token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

