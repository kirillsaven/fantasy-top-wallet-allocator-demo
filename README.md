# Fantasy Top Wallet Allocator Demo

Sanitized case study and runnable demo of a Telegram-style assistant for
Fantasy Top wallet analysis and tournament deck allocation.

The original private tool accepted a player's wallet in Telegram, reviewed that
wallet's card portfolio for the next tournament, and produced an all-league deck
allocation report. This public repository keeps that product shape while using
synthetic wallet data and a compact global allocation optimizer for the demo
fixture.

## Recruiter / Reviewer Summary

This is a sanitized portfolio demo of a private Fantasy Top strategy workflow.
It demonstrates:

- domain-to-product translation;
- wallet-to-report flow design;
- league constraint modeling;
- global deck allocation over a synthetic fixture;
- risk-adjusted scoring;
- synthetic data design;
- QA tests for legality, uniqueness, output shape, independent brute-force verification, and greedy-vs-global behavior;
- human-in-the-loop decision design.

It does not include:

- real wallets;
- live Fantasy Top API access;
- private sessions, tokens, or cookies;
- production market history;
- exact private trading logic;
- server logs or deployment details.

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
- Builds a global non-overlapping allocation across all configured leagues.
- Keeps each card exclusive across the generated tournament allocation.
- Reports unused cards separately.
- Includes tests for legality, uniqueness, bot-command handling, output shape,
  independent brute-force verification, and a counterexample where global
  allocation beats greedy allocation.

## What “global allocation” means in this demo

For the synthetic fixture, the public optimizer enumerates every legal deck
candidate for every configured league slot, then searches non-overlapping package
combinations with a bitmask dynamic-programming pass.

The demo objective is explicit and deterministic:

1. fill as many feasible deck slots as possible;
2. maximize total risk-adjusted utility;
3. maximize total projected score;
4. minimize total market cost.

This is an exact global search for the compact public fixture. It is not the full
private production allocator, which also handled live wallet ingestion, broader
market data, production heuristics, reward/EV modeling, coverage layers, and
operator-specific review logic.

## 60-second demo

```bash
python -m pip install -e ".[dev]"
fantasy-wallet-demo --telegram-message "/report demo-wallet-seven"
python -m pytest -q
```

## Quick start

```bash
python -m pip install -e ".[dev]"
python -m fantasy_strategy_demo --wallet demo-wallet-seven --fixture data/sample_wallet.json
python -m fantasy_strategy_demo --telegram-message "/report demo-wallet-seven" --fixture data/sample_wallet.json
fantasy-wallet-demo --telegram-message "/report demo-wallet-seven"
python -m pytest -q
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
- projected score: 4398
- total stars: 19

## Silver Deck 1
- projected score: 3122
- total stars: 14

## Bronze Deck 1
- projected score: 2265
- total stars: 13
```

The real command prints the full card list and unused-card section.

## How this maps to AI evaluation work

This project is relevant to AI evaluation because the workflow requires:

- checking output against domain constraints;
- detecting stale or unsupported recommendations;
- turning ambiguous domain rules into evaluation criteria;
- keeping generated recommendations human-reviewed;
- testing edge cases and failure modes.

## Original private project scope

The internal system was broader than this public demo. It included:

- wallet ingestion and portfolio reconciliation;
- tournament-aware player/hero prediction;
- all-league deck allocation and global package review;
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
