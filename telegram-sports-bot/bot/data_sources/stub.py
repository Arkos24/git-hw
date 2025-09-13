from __future__ import annotations

from datetime import datetime, timedelta
from typing import Iterable

from .base import DataSource, MatchInfo, TeamInfo


class StubDataSource(DataSource):
    async def fetch_upcoming_matches(self) -> Iterable[MatchInfo]:
        now = datetime.utcnow()
        return [
            MatchInfo(
                league="Premier League",
                home_team="Team A",
                away_team="Team B",
                start_time=now + timedelta(hours=6),
            ),
            MatchInfo(
                league="Premier League",
                home_team="Team C",
                away_team="Team D",
                start_time=now + timedelta(hours=8),
            ),
        ]

    async def fetch_team_info(self, team_name: str) -> TeamInfo | None:
        return TeamInfo(name=team_name, league="Premier League", country="GBR")

