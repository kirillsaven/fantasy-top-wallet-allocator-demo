# Fantasy Top Telegram Bot Demo

Sanitized case study and runnable demo of a Telegram-style assistant for
Fantasy Top wallet analysis and tournament deck allocation.

The original private tool accepted a player's wallet in Telegram, reviewed that
wallet's card portfolio for the next tournament, and produced an all-league deck
allocation report. This public repository keeps that product shape while using
synthetic wallet data and a compact deterministic optimizer.

## Why this exists

Competitive Web3 card games mix several hard problems:

- reading a changing card portfolio from a wallet;
- understanding the upcoming tournament and league constraints;
- estimating card strength before tournament lock;
- allocating cards across Diamond, Platinum, Gold, Silver, and Bronze decks;
- keeping card usage exclusive across the full allocation;
- balancing expected score, volatility, opportunity cost, and market liquidity;
- returning a concise Telegram-style report that a human operator can review.

This demo shows the core product thinking behind that workflow without exposing
real wallets, API sessions, market history, logs, or private heuristics.

## What the demo does

- Simulates a Telegram command such as `/report demo-wallet-seven`.
- Loads a synthetic wallet fixture from `data/sample_wallet.json`.
- Reads the upcoming tournament and all league rules.
- Scores cards with rarity, star, market, and uncertainty signals.
- Builds legal decks across all configured leagues.
- Keeps each card exclusive across the generated tournament allocation.
- Reports unused cards separately.
- Includes tests for legality, uniqueness, bot-command handling, and output
  shape.

## Quick start

```bash
python -m pip install -e ".[dev]"
python -m fantasy_strategy_demo --wallet demo-wallet-seven --fixture data/sample_wallet.json
python -m fantasy_strategy_demo --telegram-message "/report demo-wallet-seven" --fixture data/sample_wallet.json
python -m pytest -q
```

After installation, the console script is also available:

```bash
fantasy-top-bot-demo --telegram-message "/report demo-wallet-seven"
```

## Example output

```text
# Fantasy Top Wallet Allocation

Wallet: `demo-wallet-seven`
Tournament: Main Tournament Demo 109
Status: upcoming
Starts at: 2026-07-13T18:00:00Z

## Allocation summary
- decks built: 5
- cards used: 25
- cards left unused: 2

## Diamond Deck 1
- projected score: 8020
- total stars: 26

## Platinum Deck 1
- projected score: 6285
- total stars: 21

## Gold Deck 1
- projected score: 4562
- total stars: 21

## Silver Deck 1
- projected score: 3172
- total stars: 15

## Bronze Deck 1
- projected score: 2365
- total stars: 14
```

The real command prints the full card list and unused-card section.

## Original private project scope

The internal system was broader than this public demo. It included:

- wallet ingestion and portfolio reconciliation;
- tournament-aware player/hero prediction;
- all-league deck allocation;
- market scans and watchlists;
- Telegram reports for operator review;
- dashboard/API surfaces for inspection;
- regression guards and report-quality audits;
- fail-closed behavior around stale data, missing auth, or inconsistent inputs.

See [docs/case-study.md](docs/case-study.md),
[docs/architecture.md](docs/architecture.md), and
[docs/portfolio-summary.md](docs/portfolio-summary.md) for the public
case-study version.

## Sanitization

This repo intentionally excludes:

- real wallet addresses and user identifiers;
- private API tokens, sessions, and auth flows;
- server IPs, deployment paths, and operations logs;
- raw market snapshots and historical databases;
- exact private trading rules and production model artifacts.

See [docs/sanitization.md](docs/sanitization.md).

## Portfolio use

This is intended as a public portfolio artifact for AI evaluation, product
testing, Web3 strategy, Telegram bot workflows, and AI-assisted product-building
roles. It demonstrates the ability to convert domain expertise into a working,
tested decision tool.
