# Case Study: Fantasy Top Wallet Allocator

## Context

Fantasy Top combined collectible cards, social attention, tournament scoring,
league constraints, and market pricing. A useful operator tool needed to answer
a practical question quickly: given this wallet and the next tournament, how
should the cards be distributed across league decks?

The private internal system behind this demo was built to turn that workflow
into a repeatable wallet-to-report review loop with a Telegram interface.

## Role

Kirill acted as the domain expert and operator:

- defined the wallet-to-report product flow;
- translated game rules into requirements and acceptance criteria;
- reviewed model and report output against game reality;
- tested edge cases and failure modes;
- used AI-assisted development tools to iterate on scripts, dashboards, bot
  flows, and reports;
- kept the system human-reviewed before irreversible actions.

## Product responsibilities

The internal tool covered:

- wallet-based portfolio analysis;
- next-tournament context;
- hero/player signal review before tournament lock;
- all-league deck allocation and global package review;
- market and opportunity-cost checks;
- buy/hold/sell watchlists;
- Telegram reports for fast operator review;
- dashboard/API surfaces for inspection;
- fail-closed behavior when data was stale, incomplete, or inconsistent.

## What this public demo preserves

This repository preserves the public-safe shape of the problem:

- Telegram-style `/report <wallet>` command handling;
- synthetic wallet input;
- upcoming tournament context;
- league legality constraints;
- rarity, star, market, and uncertainty signals;
- global non-overlapping all-league deck allocation for the synthetic fixture;
- concise allocation report generation;
- tests around legality, uniqueness, command handling, and reproducibility.

## What was intentionally removed

The public demo removes all sensitive operating details: real wallets, live API
sessions, deployment targets, logs, private market history, exact trading
heuristics, and production model artifacts.

## Why it matters for AI evaluation roles

The project is relevant beyond Web3 because it required the same judgment loop
used in AI evaluation:

- compare model/tool output against domain reality;
- catch hallucinated or stale recommendations;
- write clear acceptance criteria;
- test edge cases;
- distinguish confidence from uncertainty;
- turn ambiguous outcomes into structured feedback.
