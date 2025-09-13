from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable


@dataclass
class TeamInfo:
    name: str
    league: str
    country: str | None = None


@dataclass
class MatchInfo:
    league: str
    home_team: str
    away_team: str
    start_time: datetime


class DataSource:
    async def fetch_upcoming_matches(self) -> Iterable[MatchInfo]:
        raise NotImplementedError

    async def fetch_team_info(self, team_name: str) -> TeamInfo | None:
        raise NotImplementedError

