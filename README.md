# Fantasy Top Strategy Bot Demo

Sanitized case study and runnable demo based on an internal decision-support system
for competitive Web3 card-game operations.

The original private tool supported live portfolio review, deck allocation, market
checks, and human approval workflows during Fantasy Top tournament cycles. This
repository is a public-safe demonstration: all data is synthetic, all private
runtime details were removed, and the optimizer is a compact educational
implementation rather than a dump of production code.

## Why this exists

Competitive Web3 card games mix several hard problems:

- building legal lineups from a changing card portfolio;
- estimating player/hero strength before a tournament locks;
- deciding whether a card is better used, held, bought, or sold;
- balancing expected score, volatility, opportunity cost, and market liquidity;
- producing an action plan that a human operator can review before any trade.

This demo shows the core product thinking behind that workflow without exposing
private wallets, API sessions, market history, logs, or proprietary heuristics.

## What the demo does

- Reads a synthetic card portfolio from `data/sample_portfolio.json`.
- Scores cards with rarity, star, market, and uncertainty signals.
- Builds one legal deck per league using a deterministic optimizer.
- Keeps card usage exclusive across the generated package.
- Produces a concise Markdown report for review.
- Includes tests that guard portfolio legality and deterministic output.

## Quick start

```bash
python -m pip install -e ".[dev]"
python -m fantasy_strategy_demo data/sample_portfolio.json
python -m pytest -q
```

## Example output

```text
# Strategy Package

## Bronze
- projected score: 3395
- risk-adjusted utility: 2976.8
- total stars: 12
- estimated market cost: 0.1060 ETH
- cards:
  - AlphaBuilder rare 3 stars (score 930)
  - SignalScout rare 3 stars (score 885)
  - MetaRunner common 2 stars (score 560)
  - DeckPilot common 2 stars (score 520)
  - StableHand common 2 stars (score 500)

## Silver
- projected score: 4195
- risk-adjusted utility: 4029.4
- total stars: 17
- estimated market cost: 0.2270 ETH
- cards:
  - TrendSniper epic 5 stars (score 1160)
  - VolatilityLab epic 5 stars (score 1080)
  - DataCloser rare 4 stars (score 975)
  - LateBreaker common 2 stars (score 510)
  - QuietEdge common 1 stars (score 470)
```

## Original project scope

The internal system was broader than this demo. It included:

- portfolio ingestion and reconciliation;
- tournament-aware player/hero prediction;
- league/deck allocation;
- market scans and watchlists;
- Telegram review/approval flows;
- dashboard/API surfaces;
- regression guards and report-quality audits;
- fail-closed behavior around missing data or authentication.

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
testing, Web3 strategy, and AI-assisted product-building roles. It demonstrates
the ability to convert domain expertise into a working, tested decision tool.
