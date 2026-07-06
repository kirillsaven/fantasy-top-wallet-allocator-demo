from __future__ import annotations

from itertools import combinations

from .models import Card, Deck, LeagueRules, StrategyPackage, ensure_unique_card_ids


def _deck_utility(cards: tuple[Card, ...], rules: LeagueRules) -> tuple[float, float, int, float]:
    score = sum(card.card_score for card in cards)
    upside = sum(card.upside for card in cards)
    downside = sum(card.downside for card in cards)
    market_cost = sum(card.market_price_eth for card in cards)
    total_stars = sum(card.stars for card in cards)

    volatility_bonus = upside * rules.risk_appetite
    downside_penalty = downside * (1.0 - rules.risk_appetite)
    market_penalty = market_cost * 125.0

    utility = score + volatility_bonus - downside_penalty - market_penalty
    return score, utility, total_stars, market_cost


def _is_legal(cards: tuple[Card, ...], rules: LeagueRules, used_card_ids: set[str]) -> bool:
    if len(cards) != rules.deck_size:
        return False
    if any(card.card_id in used_card_ids for card in cards):
        return False
    if any(rules.name not in card.eligible_leagues for card in cards):
        return False
    if sum(card.stars for card in cards) > rules.max_total_stars:
        return False
    if rules.max_market_cost_eth is not None:
        if sum(card.market_price_eth for card in cards) > rules.max_market_cost_eth:
            return False
    return True


def build_best_deck(
    cards: tuple[Card, ...],
    rules: LeagueRules,
    used_card_ids: set[str] | None = None,
) -> Deck:
    used = used_card_ids or set()
    candidates: list[Deck] = []

    for combo in combinations(cards, rules.deck_size):
        if not _is_legal(combo, rules, used):
            continue
        score, utility, total_stars, market_cost = _deck_utility(combo, rules)
        candidates.append(
            Deck(
                league=rules.name,
                cards=tuple(sorted(combo, key=lambda card: card.card_score, reverse=True)),
                score=score,
                utility=utility,
                total_stars=total_stars,
                market_cost_eth=market_cost,
            )
        )

    if not candidates:
        raise ValueError(f"no legal deck found for league: {rules.name}")

    return max(candidates, key=lambda deck: (deck.utility, deck.score, -deck.market_cost_eth))


def build_strategy_package(cards: tuple[Card, ...], leagues: tuple[LeagueRules, ...]) -> StrategyPackage:
    ensure_unique_card_ids(cards)
    used: set[str] = set()
    decks: list[Deck] = []

    for rules in leagues:
        deck = build_best_deck(cards, rules, used)
        decks.append(deck)
        used.update(deck.card_ids())

    return StrategyPackage(decks=tuple(decks))

