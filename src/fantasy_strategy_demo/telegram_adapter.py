from __future__ import annotations

import shlex
from pathlib import Path

from .io import load_wallet_fixture
from .optimizer import build_tournament_allocation


HELP_TEXT = """Fantasy Top Bot Demo

Commands:
- /report demo-wallet-seven
- /allocate demo-wallet-seven

This public demo uses synthetic wallet data. The private version accepted a real
wallet and produced a tournament deck-allocation report through Telegram.
"""


def handle_message(message_text: str, fixture_path: str | Path) -> str:
    try:
        parts = shlex.split(message_text)
    except ValueError:
        return "Could not parse command. Try: /report demo-wallet-seven"

    if not parts or parts[0] in {"/start", "/help"}:
        return HELP_TEXT

    command = parts[0].casefold()
    if command not in {"/report", "/allocate"}:
        return "Unknown command. Try: /report demo-wallet-seven"

    if len(parts) < 2:
        return "Missing wallet. Try: /report demo-wallet-seven"

    wallet = parts[1]
    tournament, cards, leagues = load_wallet_fixture(fixture_path, wallet)
    allocation = build_tournament_allocation(wallet, tournament, cards, leagues)
    return allocation.to_markdown()
