from fantasy_strategy_demo.io import load_wallet_fixture
from fantasy_strategy_demo.models import Card, LeagueRules, Tournament
from fantasy_strategy_demo.optimizer import build_greedy_tournament_allocation, build_tournament_allocation
from fantasy_strategy_demo.telegram_adapter import handle_message


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
