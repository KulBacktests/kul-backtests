# Episode 2: I Let My Cat Trade a Prop Firm Account

*Kul Backtests, episode 2.* The data behind the video: can the best trading bots on our leaderboard beat a cat that picks
every trade's side with its paw?

**Simulated / hypothetical, in-sample.** Every number here comes from TradingView backtests (1 May 2025 to 1 Oct 2026) run
through a $50K evaluation simulator. Nothing here is live trading. Not financial advice.

## Who is Kul?

Kul is the channel's cartoon cat. In this episode his "paw" is a seeded random number generator: on each of a bot's exact
trades it picks long or short, 50/50. No animal traded anything, and nobody gave a cat real money.

## The method in plain words

1. **The bots.** 146 ranked bots (strategy x market x timeframe): public TradingView scripts by other authors, strategies we
   coded from research papers or practitioner write-ups, and a few of our own. Each one takes a simulated 50K evaluation at its
   best size.
2. **The cats.** 1,000 copies of Kul per bot (146,000 in all) take that bot's exact trades. The paw picks each side; when it
   disagrees with the bot, the trade is mirrored and the cat still pays the same costs. Each cat takes 1,000 simulated
   evaluations.
3. **The luckiest cat.** One new cat on each of the 146 bots' trades, keep the luckiest, and repeat 60 times. The bots were
   picked the same way: the best of many tries, chosen after the fact.

## What is in this folder

| File | What it holds |
|---|---|
| `bots.csv` | The bot list: all 146 ranked bots, each with its **author** (TradingView username) or **research paper**, its size on the 50K evaluation, its pass odds, and the pass odds of its 1,000 cats (5th percentile, median, 95th percentile, best). `main_leaderboard_rank_150k_rank_only` is the rank on our main leaderboard (150K first-payout odds); those odds are not published here. |
| `cats/cat_runs.csv` | Every cat run: 146,000 paw-picked runs (1,000 per bot). Each cat takes the bot's exact trades and picks each side with a seeded coin flip (`paw_seed`). Pass odds and blow-up odds come from 1,000 simulated evaluations per cat. |
| `summary.json` | The headline numbers from the video in one file, read from the result files below. |
| `results/` | The numbers in the video: `pass_bars.json` (the 18 forward-test bots vs their cats), `house_cat.json` (the average cat, the zero-edge control, size, the both-years check), `luckiest_cat.json` (search #0 and the summary of all 60 searches), `searches/s_0.json` to `s_59.json` (the 146 cats of each luckiest-cat search), `funnel.json` (best of 1 / 18 / 146 / 2,594 cats), `lab_funnel.json` (how the bots were picked), `user_strategies.json` (our own strategies, including last place). |

Bots are keyed `bot001` to `bot146` by their rank on the 50K evaluation; `bots.csv` maps each key to its name and author.

## What you can check

- Every cat's pass odds, and every bot's odds next to its own 1,000 cats.
- The 60 luckiest-cat searches, and the median of 75.3% for the luckiest of 146.
- The funnel (17.4% / 49.5% / 75.3% / 89.6%) and the forward-test list vs the luckiest cat (4 of 18 stay above).
- Each headline number in the video, recomputed from these rows.

You cannot re-run the simulations from this folder: the simulator is not published (see below).

## What is not included

- **The prop simulator.** Its source code is not published.
- **The bots' code.** Each author's Pine script stays on TradingView under its author's name; strategies built from research
  papers are credited to the paper. No third-party code is in this repository.
- **Trade lists and raw market data.**

## How to read it (and the caveats)

- A cat takes the **same trades** as its bot (same entry and exit times, same stop and target). Its paw picks the side; when it
  disagrees with the bot, the trade is mirrored and the cat still pays the same costs (commission + 1 tick of slippage a fill).
- The evaluation: $50,000 account, $3,000 profit target, $2,000 end-of-day trailing drawdown, no single day more than 50% of the
  profit. The prop firm is not named.
- Each forward-test bot is compared with the **luckiest of 146 cats**. Lower-ranked bots were picked less hard than the champion,
  so that bar is strictest for them.
- Six of the 18 forward-test bots only ever buy. In a rising market, a cat that only buys at those times gets exactly their result.
- All of it is in-sample: the bots, their settings and their sizes were picked on the same 17 months. None of the 18 has
  been forward-tested yet.
- Best of 1,098 and best of 2,594 cats are approximations: every cat trades one of the 146 bots' trade sets.
- Average cat: 20.3% pass, 75.4% blow-up (146,000 cats).

## Credits: the 18 forward-test bots shown in the video

Thank you to the authors. Their code is theirs and is not in this repository; the full list of all 146 bots and their authors
or papers is in `bots.csv`.

| Bot | Strategy | Market | Author / source |
|---|---|---|---|
| bot001 | Phase Oscillator (3 ATR stop, 3R target) | NQ 3m | DefinedEdge (public TradingView script) |
| bot002 | Bitcoin-to-Gold Risk Appetite, next session long (Bouri & Demir 2025; Mourey et al. 2025 weekend rows) [paper] | ES 5m | Bouri & Demir 2025 (research paper; our own code of the paper's rule) |
| bot003 | TM 50% Fib Strategy v2.5 | NQ 1m | jferheart (public TradingView script) |
| bot007 | Cross-Asset Stress Reversal (Vojtko-Dujava 2025) [paper] | ES 1h | Vojtko & Dujava 2025 (research paper; our own code of the paper's rule) |
| bot008 | 8PM MGC Double Breakout [community] | GC 5m | Edge-Session (public TradingView script) |
| bot013 | EU-Open Long after a Volatile Asian Session (Bondarenko & Muravyev 2023) [paper] | NQ 15m | Bondarenko & Muravyev 2023 (research paper; our own code of the paper's rule) |
| bot014 | VWAP Reversal V1 (long only) | NQ 15m | DerAndi72 (public TradingView script) |
| bot021 | FOMC Cycle Even Weeks Long (Cieslak, Morse & Vissing-Jorgensen 2019) [paper] | ES 1h | Cieslak, Morse & Vissing-Jorgensen 2019 (research paper; our own code of the paper's rule) |
| bot026 | Mitchell Gold IB Pullback [practitioner] | GC 15m | Cory Mitchell (practitioner write-up; our own code of the rule) |
| bot035 | HVN Fade & Break | GC 5m | blitz_locked (public TradingView script) |
| bot036 | Pooled US Release Reaction Fade, T+30m to 15:59 (Kroner 2025, Ficura 2019) [paper] | ES 3m | Kroner 2025, Ficura 2019 (research paper; our own code of the paper's rule) |
| bot042 | _mr_beach Liquidity Sweep + VWAP V2 Trend Filter, Presets | NQ 2m | ReneHerkert (_mr_beach) (public TradingView script) |
| bot044 | Pooled US Release Reaction Fade, T+30m to 15:59 (Kroner 2025, Ficura 2019) [paper] | NQ 3m | Kroner 2025, Ficura 2019 (research paper; our own code of the paper's rule) |
| bot046 | Gold Breakout 15M Strategy [WillyAlgoTrader] | GC 1m | WillyAlgoTrader (public TradingView script) |
| bot058 | Asian Breakout - AutoBot & Visuals | GC 1m | public TradingView script; the author's username is not in our lab notes yet (tell us and we'll add it) |
| bot067 | VWAP Reversal V1 (long only) | GC 1h | DerAndi72 (public TradingView script) |
| bot072 | SuperTrend Regime Confluence | GC 15m | DefinedEdge (public TradingView script) |
| bot090 | TMO Dual Timeframe | GC 1h | Inspire_Algos (Hary) (public TradingView script) |

## Disclaimer

- Backtests and simulations are hypothetical. They use past data with assumed costs and fills, they are not real trading, and
  they do not predict future results.
- Not financial advice, and not a recommendation to trade any strategy or to buy any evaluation.
- Futures are leveraged, so you can lose more than you put in.
- The 50K evaluation rules are a typical set that we simulated ourselves. No prop firm made, sponsored or reviewed this. The
  bot authors did not make, sponsor or review it either.

Found a bug? Open an issue. Want a strategy raced next? Comment on the video.
