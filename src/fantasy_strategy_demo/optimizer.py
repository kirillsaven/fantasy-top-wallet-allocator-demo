from __future__ import annotations

from itertools import combinations

from .models import Card, Deck, LeagueRules, Tournament, TournamentAllocation, ensure_unique_card_ids


_AllocationRank = tuple[int, float, float, float]


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


def _is_legal(cards: tuple[Card, ...], rules: LeagueRules, used_card_ids: set[str] | None = None) -> bool:
    used = used_card_ids or set()
    if len(cards) != rules.deck_size:
        return False
    if any(card.card_id in used for card in cards):
        return False
    if any(rules.name not in card.eligible_leagues for card in cards):
        return False
    if sum(card.stars for card in cards) > rules.max_total_stars:
        return False
    if rules.max_market_cost_eth is not None:
        if sum(card.market_price_eth for card in cards) > rules.max_market_cost_eth:
            return False
    return True


def _candidate_decks(cards: tuple[Card, ...], rules: LeagueRules, slot: int) -> tuple[Deck, ...]:
    candidates: list[Deck] = []

    for combo in combinations(cards, rules.deck_size):
        if not _is_legal(combo, rules):
            continue
        score, utility, total_stars, market_cost = _deck_utility(combo, rules)
        candidates.append(
            Deck(
                league=rules.name,
                slot=slot,
                cards=tuple(sorted(combo, key=lambda card: card.card_score, reverse=True)),
                score=score,
                utility=utility,
                total_stars=total_stars,
                market_cost_eth=market_cost,
            )
        )

    return tuple(
        sorted(candidates, key=lambda deck: (deck.utility, deck.score, -deck.market_cost_eth), reverse=True)
    )


def build_best_deck(
    cards: tuple[Card, ...],
    rules: LeagueRules,
    slot: int,
    used_card_ids: set[str] | None = None,
) -> Deck:
    used = used_card_ids or set()
    candidates = tuple(
        deck for deck in _candidate_decks(cards, rules, slot) if not deck.card_ids().intersection(used)
    )

    if not candidates:
        raise ValueError(f"no legal deck found for league: {rules.name}")

    return max(candidates, key=lambda deck: (deck.utility, deck.score, -deck.market_cost_eth))


def _allocation_rank(decks: tuple[Deck, ...]) -> _AllocationRank:
    total_utility = sum(deck.utility for deck in decks)
    total_score = sum(deck.score for deck in decks)
    total_market_cost = sum(deck.market_cost_eth for deck in decks)
    return (len(decks), total_utility, total_score, -total_market_cost)


def _card_bitmasks(cards: tuple[Card, ...], decks: tuple[Deck, ...]) -> dict[Deck, int]:
    card_index = {card.card_id: index for index, card in enumerate(cards)}
    masks: dict[Deck, int] = {}

    for deck in decks:
        mask = 0
        for card_id in deck.card_ids():
            mask |= 1 << card_index[card_id]
        masks[deck] = mask

    return masks


def _build_all_slot_candidates(
    cards: tuple[Card, ...],
    leagues: tuple[LeagueRules, ...],
) -> tuple[tuple[Deck, ...], ...]:
    slots: list[tuple[Deck, ...]] = []
    for rules in leagues:
        for slot in range(1, rules.deck_slots + 1):
            candidates = _candidate_decks(cards, rules, slot)
            if candidates:
                slots.append(candidates)
    return tuple(slots)


def build_greedy_tournament_allocation(
    wallet: str,
    tournament: Tournament,
    cards: tuple[Card, ...],
    leagues: tuple[LeagueRules, ...],
) -> TournamentAllocation:
    """Comparison baseline: allocate league-by-league in configured order."""
    ensure_unique_card_ids(cards)
    used: set[str] = set()
    decks: list[Deck] = []

    for rules in leagues:
        for slot in range(1, rules.deck_slots + 1):
            try:
                deck = build_best_deck(cards, rules, slot, used)
            except ValueError:
                continue
            decks.append(deck)
            used.update(deck.card_ids())

    unused_cards = tuple(card for card in cards if card.card_id not in used)
    return TournamentAllocation(
        wallet=wallet,
        tournament=tournament,
        decks=tuple(decks),
        unused_cards=unused_cards,
    )


def build_tournament_allocation(
    wallet: str,
    tournament: Tournament,
    cards: tuple[Card, ...],
    leagues: tuple[LeagueRules, ...],
) -> TournamentAllocation:
    ensure_unique_card_ids(cards)
    slot_candidates = _build_all_slot_candidates(cards, leagues)
    all_candidates = tuple(deck for candidates in slot_candidates for deck in candidates)
    masks = _card_bitmasks(cards, all_candidates)

    # Exact global search for the synthetic demo fixture. The first rank element
    # keeps a full feasible allocation ahead of partial fallbacks.
    states: dict[int, tuple[_AllocationRank, tuple[Deck, ...]]] = {0: ((0, 0.0, 0.0, -0.0), tuple())}
    for candidates in slot_candidates:
        next_states = dict(states)
        for used_mask, (_, chosen_decks) in states.items():
            for deck in candidates:
                deck_mask = masks[deck]
                if used_mask & deck_mask:
                    continue
                candidate_decks = chosen_decks + (deck,)
                candidate_rank = _allocation_rank(candidate_decks)
                candidate_mask = used_mask | deck_mask
                current = next_states.get(candidate_mask)
                if current is None or candidate_rank > current[0]:
                    next_states[candidate_mask] = (candidate_rank, candidate_decks)
        states = next_states

    _, decks = max(states.values(), key=lambda item: item[0])
    used = set()
    for deck in decks:
        used.update(deck.card_ids())
    unused_cards = tuple(card for card in cards if card.card_id not in used)
    return TournamentAllocation(
        wallet=wallet,
        tournament=tournament,
        decks=decks,
        unused_cards=unused_cards,
    )
