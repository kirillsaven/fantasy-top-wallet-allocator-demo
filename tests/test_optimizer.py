from fantasy_strategy_demo.io import load_portfolio
from fantasy_strategy_demo.optimizer import build_strategy_package


def test_strategy_package_uses_cards_once():
    cards, leagues = load_portfolio("data/sample_portfolio.json")

    package = build_strategy_package(cards, leagues)

    used_ids = []
    for deck in package.decks:
        used_ids.extend(card.card_id for card in deck.cards)

    assert len(used_ids) == len(set(used_ids))


def test_decks_respect_league_rules():
    cards, leagues = load_portfolio("data/sample_portfolio.json")

    package = build_strategy_package(cards, leagues)

    rules_by_name = {rules.name: rules for rules in leagues}
    for deck in package.decks:
        rules = rules_by_name[deck.league]
        assert len(deck.cards) == rules.deck_size
        assert deck.total_stars <= rules.max_total_stars
        assert deck.market_cost_eth <= rules.max_market_cost_eth
        assert all(deck.league in card.eligible_leagues for card in deck.cards)


def test_output_is_deterministic_snapshot():
    cards, leagues = load_portfolio("data/sample_portfolio.json")

    package = build_strategy_package(cards, leagues)
    markdown = package.to_markdown()

    assert "## Bronze" in markdown
    assert "## Silver" in markdown
    assert "AlphaBuilder" in markdown
    assert "projected score" in markdown

