from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Card, LeagueRules, Tournament


def load_wallet_fixture(
    path: str | Path,
    wallet: str,
) -> tuple[Tournament, tuple[Card, ...], tuple[LeagueRules, ...]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))

    tournament_payload = _require_dict(payload, "tournament")
    tournament = Tournament(
        name=str(tournament_payload["name"]),
        starts_at=str(tournament_payload["starts_at"]),
        status=str(tournament_payload["status"]),
    )

    leagues = tuple(
        LeagueRules(
            name=str(item["name"]),
            deck_size=int(item["deck_size"]),
            max_total_stars=int(item["max_total_stars"]),
            deck_slots=int(item.get("deck_slots", 1)),
            max_market_cost_eth=(
                None
                if item.get("max_market_cost_eth") is None
                else float(item["max_market_cost_eth"])
            ),
            risk_appetite=float(item.get("risk_appetite", 0.35)),
        )
        for item in _require_list(payload, "leagues")
    )

    wallet_payload = _find_wallet_payload(payload, wallet)
    cards = tuple(_parse_card(item) for item in _require_list(wallet_payload, "cards"))

    return tournament, cards, leagues


def _parse_card(item: dict[str, Any]) -> Card:
    return Card(
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


def _find_wallet_payload(payload: dict[str, Any], wallet: str) -> dict[str, Any]:
    normalized_wallet = wallet.casefold()
    for item in _require_list(payload, "wallets"):
        if str(item.get("wallet", "")).casefold() == normalized_wallet:
            return item
    available = ", ".join(str(item.get("wallet", "")) for item in _require_list(payload, "wallets"))
    raise ValueError(f"wallet not found: {wallet}. Available demo wallets: {available}")


def _require_dict(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"expected object at key: {key}")
    return value


def _require_list(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = payload.get(key)
    if not isinstance(value, list):
        raise ValueError(f"expected list at key: {key}")
    return value
