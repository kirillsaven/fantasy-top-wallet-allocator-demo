from itertools import combinations

import pytest

from fantasy_strategy_demo.io import load_wallet_fixture
from fantasy_strategy_demo.models import Card, Deck, LeagueRules, Tournament
from fantasy_strategy_demo.optimizer import build_greedy_tournament_allocation, build_tournament_allocation
from fantasy_strategy_demo.telegram_adapter import handle_message


def _test_deck_utility(cards: tuple[Card, ...], rules: LeagueRules) -> tuple[float, float, int, float]:
    """Independent test-side copy of the public demo objective."""
    score = sum(card.card_score for card in cards)
    upside = sum(card.upside for card in cards)
    downside = sum(card.downside for card in cards)
    market_cost = sum(card.market_price_eth for card in cards)
    total_stars = sum(card.stars for card in cards)

    utility = score + upside * rules.risk_appetite - downside * (1.0 - rules.risk_appetite) - market_cost * 125.0
    return score, utility, total_stars, market_cost


def _test_candidate_decks(cards: tuple[Card, ...], rules: LeagueRules, slot: int) -> tuple[Deck, ...]:
    candidates: list[Deck] = []
    for combo in combinations(cards, rules.deck_size):
        if any(rules.name not in card.eligible_leagues for card in combo):
            continue
        if sum(card.stars for card in combo) > rules.max_total_stars:
            continue
        market_cost = sum(card.market_price_eth for card in combo)
        if rules.max_market_cost_eth is not None and market_cost > rules.max_market_cost_eth:
            continue
        score, utility, total_stars, market_cost = _test_deck_utility(combo, rules)
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
    return tuple(candidates)


def _test_allocation_rank(decks: tuple[Deck, ...]) -> tuple[int, float, float, float]:
    return (
        len(decks),
        sum(deck.utility for deck in decks),
        sum(deck.score for deck in decks),
        -sum(deck.market_cost_eth for deck in decks),
    )


def _independent_bruteforce_best_rank(
    cards: tuple[Card, ...],
    leagues: tuple[LeagueRules, ...],
) -> tuple[int, float, float, float]:
    """Exhaustive verifier for small fixtures; deliberately separate from optimizer.py."""
    slot_candidates: list[tuple[Deck, ...]] = []
    for rules in leagues:
        for slot in range(1, rules.deck_slots + 1):
            candidates = _test_candidate_decks(cards, rules, slot)
            if candidates:
                slot_candidates.append(candidates)

    best_rank: tuple[int, float, float, float] = (0, 0.0, 0.0, -0.0)

    def walk(index: int, used_card_ids: set[str], chosen: tuple[Deck, ...]) -> None:
        nonlocal best_rank
        current_rank = _test_allocation_rank(chosen)
        if current_rank > best_rank:
            best_rank = current_rank
        if index >= len(slot_candidates):
            return

        # Partial fallback path, matching the public demo contract: fill as many
        # feasible slots as possible, then optimize utility/score/cost.
        walk(index + 1, used_card_ids, chosen)

        for deck in slot_candidates[index]:
            deck_ids = deck.card_ids()
            if deck_ids.intersection(used_card_ids):
                continue
            walk(index + 1, used_card_ids | deck_ids, chosen + (deck,))

    walk(0, set(), tuple())
    return best_rank


def test_tournament_allocation_uses_cards_once():
    tournament, cards, leagues = load_wallet_fixture("data/sample_wallet.json", "demo-wallet-seven")

    allocation = build_tournament_allocation("demo-wallet-seven", tournament, cards, leagues)

    used_ids = []
    for deck in allocation.decks:
        used_ids.extend(card.card_id for card in deck.cards)

    assert len(used_ids) == len(set(used_ids))


def test_decks_respect_league_rules():
    tournament, cards, leagues = load_wallet_fixture("data/sample_wallet.json", "demo-wallet-seven")

    allocation = build_tournament_allocation("demo-wallet-seven", tournament, cards, leagues)

    rules_by_name = {rules.name: rules for rules in leagues}
    for deck in allocation.decks:
        rules = rules_by_name[deck.league]
        assert len(deck.cards) == rules.deck_size
        assert deck.total_stars <= rules.max_total_stars
        assert deck.market_cost_eth <= rules.max_market_cost_eth
        assert all(deck.league in card.eligible_leagues for card in deck.cards)


def test_output_is_wallet_bot_report():
    tournament, cards, leagues = load_wallet_fixture("data/sample_wallet.json", "demo-wallet-seven")

    allocation = build_tournament_allocation("demo-wallet-seven", tournament, cards, leagues)
    markdown = allocation.to_markdown()

    assert "Fantasy Top Wallet Allocation" in markdown
    assert "Strategy Package" not in markdown
    assert "demo-wallet-seven" in markdown
    assert "Diamond Deck 1" in markdown
    assert "Platinum Deck 1" in markdown
    assert "Gold Deck 1" in markdown
    assert "Silver Deck 1" in markdown
    assert "## Bronze" in markdown
    assert "projected score" in markdown


def test_output_is_deterministic():
    tournament, cards, leagues = load_wallet_fixture("data/sample_wallet.json", "demo-wallet-seven")

    first = build_tournament_allocation("demo-wallet-seven", tournament, cards, leagues).to_markdown()
    second = build_tournament_allocation("demo-wallet-seven", tournament, cards, leagues).to_markdown()

    assert first == second
    assert first.index("## Diamond Deck 1") < first.index("## Platinum Deck 1")
    assert first.index("## Platinum Deck 1") < first.index("## Gold Deck 1")


def test_telegram_report_command_returns_allocation():
    response = handle_message("/report demo-wallet-seven", "data/sample_wallet.json")

    assert "Fantasy Top Wallet Allocation" in response
    assert "Wallet: `demo-wallet-seven`" in response
    assert "Tournament: Main Tournament Demo 109" in response


def test_global_optimizer_matches_independent_bruteforce_on_small_fixture():
    tournament = Tournament(name="Bruteforce Cup", starts_at="2026-07-13T18:00:00Z", status="upcoming")
    leagues = (
        LeagueRules(name="Alpha", deck_size=2, max_total_stars=4, risk_appetite=0.40),
        LeagueRules(name="Beta", deck_size=2, max_total_stars=4, risk_appetite=0.35),
        LeagueRules(name="Gamma", deck_size=2, max_total_stars=4, risk_appetite=0.30),
    )
    cards = (
        Card("shared_a", "SharedA", "common", 2, 120, 150, 95, 0.01, ("Alpha", "Beta")),
        Card("shared_b", "SharedB", "rare", 2, 100, 140, 70, 0.02, ("Alpha", "Gamma")),
        Card("alpha_only", "AlphaOnly", "common", 1, 95, 110, 85, 0.00, ("Alpha",)),
        Card("beta_only", "BetaOnly", "common", 1, 94, 108, 84, 0.00, ("Beta",)),
        Card("gamma_only", "GammaOnly", "common", 1, 93, 107, 83, 0.00, ("Gamma",)),
        Card("beta_gamma", "BetaGamma", "rare", 2, 90, 130, 65, 0.02, ("Beta", "Gamma")),
    )

    allocation = build_tournament_allocation("demo", tournament, cards, leagues)
    actual_rank = _test_allocation_rank(allocation.decks)
    expected_rank = _independent_bruteforce_best_rank(cards, leagues)

    assert actual_rank[0] == expected_rank[0]
    assert actual_rank[1] == pytest.approx(expected_rank[1])
    assert actual_rank[2] == pytest.approx(expected_rank[2])
    assert actual_rank[3] == pytest.approx(expected_rank[3])


def test_global_optimizer_beats_greedy_counterexample():
    tournament = Tournament(name="Counterexample Cup", starts_at="2026-07-13T18:00:00Z", status="upcoming")
    leagues = (
        LeagueRules(name="Alpha", deck_size=1, max_total_stars=10),
        LeagueRules(name="Beta", deck_size=1, max_total_stars=10),
    )
    cards = (
        Card(
            card_id="shared",
            handle="SharedCarry",
            rarity="common",
            stars=1,
            projected_score=100,
            upside_score=100,
            downside_score=100,
            market_price_eth=0,
            eligible_leagues=("Alpha", "Beta"),
        ),
        Card(
            card_id="alpha_only",
            handle="AlphaOnly",
            rarity="common",
            stars=1,
            projected_score=99,
            upside_score=99,
            downside_score=99,
            market_price_eth=0,
            eligible_leagues=("Alpha",),
        ),
        Card(
            card_id="beta_only",
            handle="BetaOnly",
            rarity="common",
            stars=1,
            projected_score=1,
            upside_score=1,
            downside_score=1,
            market_price_eth=0,
            eligible_leagues=("Beta",),
        ),
    )

    greedy = build_greedy_tournament_allocation("demo", tournament, cards, leagues)
    global_allocation = build_tournament_allocation("demo", tournament, cards, leagues)

    greedy_utility = sum(deck.utility for deck in greedy.decks)
    global_utility = sum(deck.utility for deck in global_allocation.decks)

    assert global_utility > greedy_utility
    assert global_allocation.decks[0].cards[0].card_id == "alpha_only"
    assert global_allocation.decks[1].cards[0].card_id == "shared"


def test_unknown_wallet_fails_cleanly():
    try:
        load_wallet_fixture("data/sample_wallet.json", "missing-wallet")
    except ValueError as exc:
        assert "wallet not found" in str(exc)
    else:
        raise AssertionError("missing wallet should fail")


def test_malformed_fixture_fails_cleanly(tmp_path):
    fixture = tmp_path / "malformed.json"
    fixture.write_text("{}", encoding="utf-8")

    try:
        load_wallet_fixture(fixture, "demo-wallet-seven")
    except ValueError as exc:
        assert "expected object at key: tournament" in str(exc)
    else:
        raise AssertionError("malformed fixture should fail")
