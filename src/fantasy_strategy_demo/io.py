from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Card, LeagueRules


def load_portfolio(path: str | Path) -> tuple[tuple[Card, ...], tuple[LeagueRules, ...]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))

    cards = tuple(
        Card(
            card_id=str(item["card_id"]),
            handle=str(item["handle"]),
            rarity=str(item["rarity"]),
            stars=int(item["stars"]),
            projected_score=float(item["projected_score"]),
            upside_score=float(item["upside_score"]),
            downside_score=float(item["downside_score"]),
            market_price_eth=float(item["market_price_eth"]),
            eligible_leagues=tuple(str(value) for value in item["eligible_leagues"]),
        )
        for item in _require_list(payload, "cards")
    )

    leagues = tuple(
        LeagueRules(
            name=str(item["name"]),
            deck_size=int(item["deck_size"]),
            max_total_stars=int(item["max_total_stars"]),
            max_market_cost_eth=(
                None
                if item.get("max_market_cost_eth") is None
                else float(item["max_market_cost_eth"])
            ),
            risk_appetite=float(item.get("risk_appetite", 0.35)),
        )
        for item in _require_list(payload, "leagues")
    )

    return cards, leagues


def _require_list(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = payload.get(key)
    if not isinstance(value, list):
        raise ValueError(f"expected list at key: {key}")
    return value

