# Portfolio Summary

## One-line positioning

Telegram-style Fantasy Top wallet bot demo for upcoming-tournament deck
allocation across all leagues.

## Public description

Fantasy Top Telegram Bot Demo is a sanitized public version of a private
operator tool used for competitive Web3 card-game strategy. The original system
accepted a wallet in Telegram, analyzed the player's card portfolio for the next
tournament, allocated cards across league decks, and returned a reviewable
report.

This repository keeps the product shape visible while replacing private wallet
data, API sessions, and market history with synthetic fixtures and a compact
deterministic optimizer.

## What to review

- `README.md` for quick start and sample bot output.
- `src/fantasy_strategy_demo/telegram_adapter.py` for Telegram-style command
  handling.
- `src/fantasy_strategy_demo/optimizer.py` for the deck allocation logic.
- `data/sample_wallet.json` for synthetic wallet and tournament input.
- `tests/test_optimizer.py` for legality, uniqueness, and command tests.
- `docs/case-study.md` for the role, workflow, and AI evaluation relevance.

## Skills demonstrated

- Domain-to-product translation.
- Telegram bot workflow design.
- AI-assisted prototyping and iteration.
- Structured evaluation of model/tool output.
- Manual QA mindset around legality, edge cases, and stale data.
- Web3 gaming economy analysis.
- Human-in-the-loop decision design.

## LinkedIn-ready project blurb

Built a sanitized public demo of a Fantasy Top Telegram bot that accepts a demo
wallet, reads upcoming tournament context, and allocates cards across Diamond,
Platinum, Gold, Silver, and Bronze decks with legality checks, risk-adjusted
scoring, market-cost awareness, deterministic output, and tests. The private
version supported live wallet review, broader market checks, and human approval
workflows during tournament cycles.
