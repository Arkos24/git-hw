from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BetRecommendation:
    selection: str
    edge: float
    stake: float


def kelly_fraction(prob: float, odds: float, fraction: float = 0.5) -> float:
    # Kelly: f* = (bp - q)/b, where b = odds-1, p = prob, q = 1-p
    if odds <= 1.0:
        return 0.0
    b = odds - 1.0
    p = prob
    q = 1.0 - p
    k = (b * p - q) / b
    return max(0.0, k * fraction)


def flat_stake(bankroll: float, unit: float = 0.01) -> float:
    return max(0.0, bankroll * unit)


def recommend_stake(strategy: str, bankroll: float, prob: float, odds: float) -> float:
    if strategy == "kelly":
        return bankroll * kelly_fraction(prob, odds)
    if strategy == "kelly_half":
        return bankroll * kelly_fraction(prob, odds, fraction=0.5)
    return flat_stake(bankroll)

