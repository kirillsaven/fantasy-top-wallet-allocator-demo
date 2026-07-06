from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


RARITY_MULTIPLIERS = {
    "common": 1.0,
    "rare": 1.5,
    "epic": 2.0,
    "legendary": 2.5,
}


@dataclass(frozen=True)
class Card:
    card_id: str
    handle: str
    rarity: str
    stars: int
    projected_score: float
    upside_score: float
    downside_score: float
    market_price_eth: float
    eligible_leagues: tuple[str, ...]

    @property
    def rarity_multiplier(self) -> float:
        try:
            return RARITY_MULTIPLIERS[self.rarity]
        except KeyError as exc:
            raise ValueError(f"unknown rarity: {self.rarity}") from exc

    @property
    def card_score(self) -> float:
        return self.projected_score * self.rarity_multiplier

    @property
    def upside(self) -> float:
        return max(0.0, self.upside_score - self.projected_score) * self.rarity_multiplier

    @property
    def downside(self) -> float:
        return max(0.0, self.projected_score - self.downside_score) * self.rarity_multiplier


@dataclass(frozen=True)
class LeagueRules:
    name: str
    deck_size: int
    max_total_stars: int
    max_market_cost_eth: float | None = None
    risk_appetite: float = 0.35


@dataclass(frozen=True)
class Deck:
    league: str
    cards: tuple[Card, ...]
    score: float
    utility: float
    total_stars: int
    market_cost_eth: float

    def card_ids(self) -> set[str]:
        return {card.card_id for card in self.cards}


@dataclass(frozen=True)
class StrategyPackage:
    decks: tuple[Deck, ...]

    def used_card_ids(self) -> set[str]:
        used: set[str] = set()
        for deck in self.decks:
            used.update(deck.card_ids())
        return used

    def to_markdown(self) -> str:
        lines = ["# Strategy Package", ""]
        for deck in self.decks:
            lines.extend(
                [
                    f"## {deck.league}",
                    f"- projected score: {deck.score:.0f}",
                    f"- risk-adjusted utility: {deck.utility:.1f}",
                    f"- total stars: {deck.total_stars}",
                    f"- estimated market cost: {deck.market_cost_eth:.4f} ETH",
                    "- cards:",
                ]
            )
            for card in deck.cards:
                lines.append(
                    f"  - {card.handle} {card.rarity} {card.stars} stars "
                    f"(score {card.card_score:.0f})"
                )
            lines.append("")
        return "\n".join(lines).rstrip() + "\n"


def ensure_unique_card_ids(cards: Iterable[Card]) -> None:
    seen: set[str] = set()
    for card in cards:
        if card.card_id in seen:
            raise ValueError(f"duplicate card_id: {card.card_id}")
        seen.add(card.card_id)

