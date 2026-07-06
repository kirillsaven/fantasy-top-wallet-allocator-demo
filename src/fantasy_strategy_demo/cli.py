from __future__ import annotations

import argparse

from .io import load_portfolio
from .optimizer import build_strategy_package


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a synthetic Fantasy Top strategy package.")
    parser.add_argument("portfolio", help="Path to a synthetic portfolio JSON file.")
    args = parser.parse_args()

    cards, leagues = load_portfolio(args.portfolio)
    package = build_strategy_package(cards, leagues)
    print(package.to_markdown())


if __name__ == "__main__":
    main()

