from __future__ import annotations

from dataclasses import dataclass
from math import exp
from typing import Dict, Tuple


@dataclass
class EloRating:
    k_factor: float = 20.0
    base: float = 400.0

    ratings: Dict[str, float] | None = None

    def __post_init__(self):
        if self.ratings is None:
            self.ratings = {}

    def expected_score(self, rating_a: float, rating_b: float) -> float:
        return 1.0 / (1.0 + 10 ** ((rating_b - rating_a) / self.base))

    def get_rating(self, team: str) -> float:
        return self.ratings.get(team, 1500.0)

    def update(self, team_a: str, team_b: str, outcome_a: float) -> Tuple[float, float]:
        ra = self.get_rating(team_a)
        rb = self.get_rating(team_b)
        ea = self.expected_score(ra, rb)
        eb = 1 - ea
        ra_new = ra + self.k_factor * (outcome_a - ea)
        rb_new = rb + self.k_factor * ((1 - outcome_a) - eb)
        self.ratings[team_a] = ra_new
        self.ratings[team_b] = rb_new
        return ra_new, rb_new

    def predict_win_prob(self, home_team: str, away_team: str) -> Tuple[float, float, float]:
        ra = self.get_rating(home_team)
        rb = self.get_rating(away_team)
        p_home = self.expected_score(ra + 50.0, rb)  # simple home advantage
        p_away = 1 - self.expected_score(ra, rb + 50.0)
        p_draw = max(0.0, 1.0 - p_home - p_away)
        total = p_home + p_draw + p_away
        return p_home / total, p_draw / total, p_away / total


def poisson_goal_prob(lambda_goals: float, k: int) -> float:
    # P(X=k) = e^-λ * λ^k / k!
    # compute factorial iteratively to avoid importing math.factorial
    factorial = 1
    for i in range(2, k + 1):
        factorial *= i
    return exp(-lambda_goals) * (lambda_goals ** k) / factorial


def predict_score_probs(home_goals: float, away_goals: float) -> Dict[Tuple[int, int], float]:
    probs: Dict[Tuple[int, int], float] = {}
    for h in range(0, 6):
        for a in range(0, 6):
            probs[(h, a)] = poisson_goal_prob(home_goals, h) * poisson_goal_prob(away_goals, a)
    return probs

