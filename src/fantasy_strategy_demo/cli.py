from __future__ import annotations

import argparse

from .io import load_wallet_fixture
from .optimizer import build_tournament_allocation
from .telegram_adapter import handle_message


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a sanitized Fantasy Top wallet bot demo.")
    parser.add_argument(
        "--fixture",
        default="data/sample_wallet.json",
        help="Path to a synthetic wallet fixture JSON file.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--wallet", help="Demo wallet to allocate for the upcoming tournament.")
    mode.add_argument(
        "--telegram-message",
        help='Simulate a Telegram bot message, for example: "/report demo-wallet-seven".',
    )
    args = parser.parse_args()

    if args.telegram_message:
        print(handle_message(args.telegram_message, args.fixture))
        return

    wallet = args.wallet or "demo-wallet-seven"
    tournament, cards, leagues = load_wallet_fixture(args.fixture, wallet)
    allocation = build_tournament_allocation(wallet, tournament, cards, leagues)
    print(allocation.to_markdown())


if __name__ == "__main__":
    main()
