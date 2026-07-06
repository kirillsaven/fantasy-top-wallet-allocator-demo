# Case Study: Web3 Card-Game Decision Support

## Context

Fantasy Top combined collectible cards, social attention, tournament scoring, and
market pricing. Good operators had to understand both gameplay and trading:
which cards were likely to score, which decks were legal, where market prices
were misaligned, and when uncertainty made a move too risky.

The private internal system behind this demo was built to turn that workflow into
a repeatable review loop.

## Role

Kirill acted as the domain expert and operator:

- defined the strategy and product requirements;
- reviewed model and report output against game reality;
- tested edge cases and failure modes;
- used AI-assisted development tools to iterate on scripts, dashboards, and
  reports;
- kept the system human-reviewed before any irreversible action.

## Product responsibilities

The internal tool covered:

- portfolio analysis from a player's card inventory;
- hero/player signal review before tournament lock;
- deck allocation across multiple leagues;
- market and opportunity-cost checks;
- buy/hold/sell watchlists;
- Telegram-style reports for fast operator review;
- dashboard/API surfaces for inspection;
- fail-closed behavior when data was stale, incomplete, or inconsistent.

## What this public demo preserves

This repository preserves the public-safe shape of the problem:

- synthetic portfolio input;
- league legality constraints;
- rarity, star, market, and uncertainty signals;
- deterministic deck package construction;
- concise report generation;
- tests around legality and reproducibility.

## What was intentionally removed

The public demo removes all sensitive operating details: real wallets, live API
sessions, deployment targets, logs, private market history, and exact trading
heuristics.

## Why it matters for AI evaluation roles

The project is relevant beyond Web3 because it required the same judgment loop
used in AI evaluation:

- compare model output against domain reality;
- catch hallucinated or stale recommendations;
- write clear acceptance criteria;
- test edge cases;
- distinguish confidence from uncertainty;
- turn ambiguous outcomes into structured feedback.

