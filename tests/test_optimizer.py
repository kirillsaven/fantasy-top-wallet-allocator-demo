from fantasy_strategy_demo.io import load_wallet_fixture
from fantasy_strategy_demo.optimizer import build_tournament_allocation
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


def test_telegram_report_command_returns_allocation():
    response = handle_message("/report demo-wallet-seven", "data/sample_wallet.json")

    assert "Fantasy Top Wallet Allocation" in response
    assert "Wallet: `demo-wallet-seven`" in response
    assert "Tournament: Main Tournament Demo 109" in response
