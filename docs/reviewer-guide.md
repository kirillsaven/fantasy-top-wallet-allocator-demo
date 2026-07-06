# Reviewer Guide

## What to inspect

- `README.md` for the product summary and demo commands.
- `data/sample_wallet.json` for the synthetic wallet and tournament fixture.
- `src/fantasy_strategy_demo/telegram_adapter.py` for Telegram-style command
  handling.
- `src/fantasy_strategy_demo/optimizer.py` for candidate deck generation and
  global non-overlapping allocation.
- `tests/test_optimizer.py` for legality, uniqueness, output, and
  greedy-vs-global regression coverage.

## Commands to run

```bash
python -m pip install -e ".[dev]"
fantasy-wallet-demo --telegram-message "/report demo-wallet-seven"
python -m pytest -q
python scripts/check_no_secrets.py
```

## What this demo proves

- A wallet-to-report workflow can be modeled with synthetic data.
- League rules and card uniqueness can be enforced in tests.
- A global allocation search can beat greedy league-by-league allocation.
- The output is structured for human review rather than automatic execution.

## What this demo does not prove

- Live Fantasy Top API access.
- Real wallet ingestion.
- Production market history or private trading heuristics.
- Original private system performance.
- Automated registration of real tournament decks.
