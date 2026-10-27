# EMA9 x VWAP claim test (Kul Backtests, episode 1)

The material behind "Using an Instagram Reel to Pass a Prop Firm".

- `SPEC_preregistration.md`: the rule as spoken in the reel, the costs, and the pass bar and checks we wrote down BEFORE running anything.
- `pine/rl-ema9-vwap-cross.pine`: our TradingView Pine v6 port of the rule. It is not the reel's or RoboQuant's code; we never saw theirs.
  - **Known bug (bug included, as promised):** around line 489, a cross on the last bar of an early-close session, taken while flat, would fill at the next session's open (the check `not session.islastbar` is missing). It never triggered in our tests.
- `REPORT.md`: the full result write-up.
- `results/`: TradingView Strategy Lab exports (`labRes14_export.json` summary rows; `labTrades14_export.json` every trade, 1 May 2025 to 1 Oct 2026) and the numbers used in the episode (`episode_*.json`: claims, results, equity curves, the 1,000-coin-flip Monte Carlo, costs, prop-evaluation odds).
- `EPISODE_NUMBERS.md`: every number said or shown in the video, with its source.

Not included: raw market data (it is licensed and can't be redistributed).

Not financial advice. Backtests and simulations are hypothetical, not live trading results. Futures can lose more than you invest.

## Redactions
Local file paths and a private TradingView layout link were replaced with placeholders (`<lab>/`, `<desktop>/`, "a private TradingView layout"). Nothing else in the pre-registration was changed.
