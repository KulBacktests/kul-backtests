# Episode 3: I Let an AI Build My Trading Strategy

*Kul Backtests, episode 3.* Video: YOUTUBE_LINK

We gave an AI coding agent a rulebook, five years of 1-minute Nasdaq futures (NQ) data and one job: find a strategy that
survives out-of-sample and sensitivity testing, not one that looks best in-sample. It started from a plain
opening-range breakout it was handed (try 1), wrote six more versions of it (tries 2 to 7), kept a journal, stopped itself when its rules said so, and then found a bug in its own winner.

This folder holds the AI's journal, all seven strategy files (the baseline it was given and the six it wrote), its Pine
port, its trade lists, and the numbers from the video.

Built by Claude Code (Anthropic's coding agent) in one session of about 20 minutes.

That session was on 18 Sep 2026; the file times run from 22:47 to 23:07. The model version was not recorded in any file, so
we don't name one.

**Backtests only.** Nothing here was traded live. Every number is a backtest or a simulation on past data, with assumed
costs and fills. Dollar figures are backtest dollars, not profit. Not financial advice.

## The verdict

**Not proven. Not yet.**

- Try 7 passes every gate the AI was given: 223 in-sample trades, profit factor 1.29, out-of-sample 72 trades at 1.46, no
  fragile parameter.
- Its side picks beat 973 of 1,000 coin-flip Kuls on the same trades. So it is not random.
- But it took 7 tries. The luckiest of 7 Kuls beats try 7's profit factor about 1 time in 6 (17.4%).
- Its in-sample profit factor falls every year: 1.83, 1.44, 1.11, 0.98.
- Its "future" test overlapped our sealed vault for 8 of 17 months. Inside the vault, try 6 was roughly flat until five
  trades in January 2026.

The test that would settle it is forward: new data the AI has never seen.

## Costs and fills

Every result uses the AI's scoring harness with these settings. The rulebook told it not to change costs, splits or gates
without telling the user, and never to make the fills kinder.

- 1 NQ contract, $20 a point.
- $5 commission per round trip.
- 1.5 ticks of slippage per side (entry and exit).
- A signal is decided on a bar's close and filled at the next bar's open.
- If one bar touches both the stop and the target, the stop is assumed to fill first.
- Flat by 15:58 New York time, and at most 240 one-minute bars in a trade.
- In-sample: 1 Sep 2021 to 31 Aug 2024. Out-of-sample: 1 Sep 2024 to 28 Jan 2026 (the end of the data).

The gates, from `CLAUDE.md.txt` and the harness: at least 200 in-sample trades; in-sample profit factor at least 1.25;
out-of-sample profit factor at least 1.15, and no more than 40% below in-sample; no parameter flagged "fragile" in the
sensitivity test; explainable to a trader in two sentences.

Profit factor (PF) is dollars won divided by dollars lost. 1.00 is break-even.

## The seven tries

In-sample, 1 NQ, after costs. Net is backtest dollars.

| Try | File | The idea (one change per try) | Trades | PF | Net | Gate |
|---|---|---|---|---|---|---|
| 1 | `v001_orb.py` | Breakout of the first 15 minutes, on the VWAP side. Stop at mid-range, target 2x the risk | 889 | 0.98 | -12,170 | fail (PF) |
| 2 | `v002_orb_atrnorm.py` | Range-size filter scaled to recent volatility | 907 | 0.95 | -25,462 | fail (PF) |
| 3 | `v003_orb_rvol.py` | Back to try 1, only on busy mornings (opening volume at least 1.2x its 14-day average) | 444 | 1.13 | +33,260 | fail (PF) |
| 4 | `v004_orb_rvol_gap.py` | Busy mornings, and only in the direction of the overnight gap | 180 | 1.47 | +41,478 | fail (under 200 trades) |
| 5 | `v005_orb_rvol_gap_noon.py` | Try 4 with entries allowed until noon | 194 | 1.35 | +34,828 | fail (under 200 trades) |
| 6 | `v006_orb_rvol1_gap.py` | Try 4 with the volume rule relaxed to "above average" (1.0x) | 307 | 1.26 | +40,915 | **pass** |
| 7 | `v007_orb_rvol1_gap_fixdays.py` | Try 6 with the Monday bug fixed | 223 | 1.29 | +34,822 | **pass** |

We re-ran every try from its code, and each trade list matched the AI's saved file trade for trade (7 of 7).

Try 6 passed at PF 1.258 against a 1.25 gate. The AI's own note: "IS PF 1.26 is a hair over the gate". Out-of-sample it
made 108 trades at PF 1.51. Its rules said to stop and report. It stopped.

## The Monday bug

While porting try 6 to TradingView Pine, the AI found that try 6 had never traded on a Monday.

It had built its day-by-day numbers over every calendar date, including Sunday evenings and holidays, which have overnight
bars but no 9:30-16:00 session. On a Monday, "yesterday's close" was Sunday's, which doesn't exist. The overnight gap came
out blank and the day was skipped. The same empty dates dragged the 14-day volume average down, so "above average" really
meant about 0.83x average.

157 of 775 in-sample sessions could never be traded: all 152 Mondays and 5 days after holidays. Tries 4 and 5 had the same
blind spot. Try 7 fixes it. It gains 40 Monday trades (PF 0.92) and still passes every gate.

The AI found this after it had written its summary naming try 6 the best candidate. That is why round 8 sits under the
summary in `journal.md`.

## The vault overlap

We keep a sealed vault: every NQ bar from 1 June 2025 on, saved for a final exam. The harness's out-of-sample window ran to
January 2026, so 8 of its 17 months were inside the vault.

The AI saw the overlap at its data check, before round 0, and wrote it down. It kept the split because its rules said not
to change it without telling the user. It then ran the out-of-sample test on three versions (tries 4, 6 and 7). No setting in the
files was changed because of what it saw.

From the AI's own saved file, `trades/trades_v006_oos.csv`:

| Try 6, out-of-sample | Trades | PF | Net (1 NQ) |
|---|---|---|---|
| Before the vault (Sep 2024 to May 2025) | 53 | 1.93 | +26,295 |
| Inside the vault (Jun 2025 to Jan 2026) | 55 | 1.18 | +6,355 |
| Inside, Jun to Dec 2025 | 50 | 0.99 | -420 |
| Inside, Jan 2026 | 5 | 5.13 | +6,775 |

For this strategy, the vault is no longer sealed.

## Kul, the control group

Kul is the channel's cartoon cat. Here his paw is a seeded coin flip. He takes the AI's exact in-sample trades (same
entries, exits, stops and targets) and picks only the side. When he disagrees with the AI, the trade is mirrored and he
still pays the same costs. There are 1,000 Kuls per version.

- On try 7's trades the median Kul has PF 0.96. The AI's 1.29 beats 973 of the 1,000 (try 6 beats 983).
- 45 of 1,000 Kuls pass the AI's own 1.25 profit-factor gate on try 7's trades (try 6: 18).
- Seven tries means seven cats. The luckiest of 7 beats try 7's PF 17.4% of the time. The luckiest of 146 (Episode 2's bot
  count) beats it 98.2% of the time.
- Buying every trade gives PF 0.73 on try 7's trades. Doing the opposite of the AI also gives 0.73.

## The 50K evaluation

A typical $50K evaluation: $3,000 profit target, $2,000 end-of-day trailing drawdown, a 50% consistency rule, at least 2
trading days, capped at 252 trading days. 5,000 simulated runs built from 5-day blocks of the 775 in-sample sessions. The
sims keep the harness fills (1.5 ticks per side, stop first) but charge the evaluation's own commission, $1.90 per micro
round trip, instead of $5 per NQ. The prop firm is not named.

- Try 7 at 1 micro: 8.4% pass, 3.3% blow-up, 88.2% still going after a year. In this backtest it earns about $1,000 a year
  at 1 micro, against a $3,000 target.
- Started on each of the 775 real days in their real order, try 7 at 1 micro never reached the target within 252 trading
  days (0 of 775).
- At its best size, 3 micros: 46.9% pass, 52.0% blow-up. The median Kul at 3 micros: 22.0% pass, 77.3% blow-up. That size
  was picked on the same data.

## What is in this folder

| Path | What it holds |
|---|---|
| `CLAUDE.md.txt` | The rulebook the AI was given: the loop, the gates, the hard rules, and when to stop and report. |
| `KICKOFF_PROMPT.md` | The prompt that started the session. |
| `journal.md` | The AI's research journal, verbatim: the data check, one entry per round, its session summary, then round 8 and the bug. |
| `results.md` | The harness's log, one row per logged run. Written by the harness, not by hand. |
| `strategies/v001_orb.py` to `v007_orb_rvol1_gap_fixdays.py` | The seven versions, unchanged. v001 is the baseline it was given; the AI wrote v002 to v007. From try 2 on, each docstring names its parent and the one thing it changed. |
| `pine/nq_orb_gap_rvol_v007.pine` | The AI's TradingView Pine v6 port of try 7. |
| `trades/trades_v001.csv` to `trades_v007.csv` | Every in-sample trade of each try (Sep 2021 to Aug 2024). |
| `trades/trades_v006_oos.csv` | Try 6's 108 out-of-sample trades (Sep 2024 to Jan 2026). Try 7's out-of-sample trade list was never saved. |
| `results/attempts.json` | The gates, then all 7 tries: idea, change, stats, gate and why, PF by year, trades by weekday, long vs short, exits, 50K odds. |
| `results/monday_bug.json` | The bug: what, how it was found, weekday counts, before and after, and the exact code lines. |
| `results/oos_holdout.json` | The windows, every out-of-sample look with its time, whether anything was tuned on it, and try 6 split before and inside the vault. |
| `results/kul_mirror.json` | 1,000 Kuls per version (tries 6 and 7): PF and net bands, histograms, the AI's percentile, luckiest-of-N, 50K odds, controls. |
| `results/prop_50k.json` | The 50K rules and the odds for all 7 tries at every size, plus the median Kul. |
| `results/equity_curves.json` | The 7 in-sample equity curves (downsampled), try 6 out-of-sample, and the AI vs Kul race. |

## How to read the files

- **Start with `journal.md`** and read it top to bottom. Round 8 comes after the session summary because the AI found the
  bug after it had stopped.
- **The trade lists** (`trades/*.csv`) have one row per trade:
  - `entry_time`, `exit_time`: New York time, with the UTC offset.
  - `side`: 1 is long, -1 is short.
  - `entry`, `exit`: fill prices, slippage included.
  - `pnl`: backtest dollars at 1 NQ, after the $5 commission.
  - `bars`: one-minute bars in the trade.
  - `reason`: `stop`, `target` or `time` (the 15:58 flatten or the 240-bar cap).
- **`results.md`** is a raw log. The harness wrote each run's stats with `|` between them, so the table falls apart on
  GitHub; read it as text. Try 1 was run with `--no-log`, so its numbers are in the journal, not here. Some versions have
  more than one row, one per run.
- **The journal's shorthand:** IS is in-sample, OOS is out-of-sample, PF is profit factor, rvol is opening-range volume
  divided by its 14-day average, R is the trade's risk (entry to stop), maxDD is maximum drawdown.
- **The strategy files** each define `PARAMS` and `generate_signals(df, params)`. A signal is decided on a bar's close and
  filled at the next bar's open. To get trades out of them you need the harness and 1-minute NQ data, and neither is here
  (see below).
- **The Pine port** was written without being compiled in TradingView; the AI says so in the file and in the journal.
  TradingView's fills are more generous than the harness. It has an input that switches the Monday bug back on ("Skip days
  after a non-session day (replicates v006)"), off by default.
- **The JSON files** hold the numbers in the video. Most start with a `note` or `method` field. Dollars are backtest dollars
  at 1 NQ unless a field says micro (`1MNQ`).

## What is not included

- **Raw market data.** The NQ 1-minute bars are licensed Databento data and can't be redistributed. There are no bar,
  tick or price files in this folder, only the AI's trade lists.
- **The scoring harness (`backtest.py`).** It contains our bar-by-bar fill simulator, and we don't publish simulator code.
  Its settings are all listed under "Costs and fills" above. The strategy files don't import it; the harness loads them and
  turns their signals into trades.
- **The 50K evaluation simulator.** Same as Episodes 1 and 2: the results are here, the source code is not.
- **Helper scripts.** A small trade-breakdown script from the session, and our own rebuild and cross-check scripts.

## Caveats

- **In-sample selection.** 7 versions, plus 96 sensitivity settings and 3 Monte Carlos run as checks. The gate itself was
  the selection pressure.
- **A marginal pass.** Try 6 scored PF 1.258 against 1.25. In its own sensitivity test, a 0.9 volume rule gives PF 1.15 and
  a 16-minute opening range gives 1.16. Neither counts as "fragile" by the harness's definition (a drop of more than 25%),
  but both would fail the gate. For try 7, a 16-minute range gives 1.11.
- **The fade.** In-sample PF by year, try 6: 1.87, 1.40, 1.11, 1.00. Try 7: 1.83, 1.44, 1.11, 0.98. 2021 is Sep to Dec
  only, and 2024 is Jan to Aug only.
- **Long vs short flips.** Shorts carried in-sample and longs carried out-of-sample. The AI refused to condition on it: "a
  long/short switch is exactly the kind of parameter that looks structural and is sample noise."
- **"Looked at twice."** The journal says the out-of-sample window was looked at twice. That was true when it was written.
  Round 8 then ran it on try 7 as well.
- **A soft leak.** After try 4's out-of-sample result (PF 1.67) the AI wrote "edge looks real" and kept building on that
  idea. No number was tuned on it, but the choice of branch was informed by the future.
- **One bar later.** Shifting every entry one bar later gives try 6 an in-sample PF of 1.25, so the result doesn't look
  like lookahead.
- **Not live.** None of this has traded on a live feed or with real money.

## Why the rulebook is a .txt file

`CLAUDE.md.txt` is the AI's rulebook exactly as it was given (its own files call it `CLAUDE.md`). We added `.txt` so that
Claude Code doesn't load it as instructions for your own session when you open this folder.

## Credits

- `strategies/v002` to `v007`, `pine/`, `trades/` and the round entries in `journal.md` were written by the AI. `strategies/v001_orb.py`
  is the baseline it was given. `results.md` was written by its harness.
- `CLAUDE.md.txt` and `KICKOFF_PROMPT.md` are the rules and the prompt it was given.
- `results/` holds our numbers for the video, built from the files above.
- The idea is a generic opening-range breakout. The AI's try 3 docstring cites a published opening-range study for the
  volume filter. We have not checked that citation.

## Redactions

The AI's files are copied verbatim, and none of them needed a change. In `results/prop_50k.json`, one field
(`rules.engine`) named a local file path and our private simulator files. It now says "the channel's own 50K evaluation
simulator". Nothing else was changed.

## Disclaimer

- Backtests and simulations are hypothetical. They use past data with assumed costs and fills, they are not real trading,
  and they do not predict future results.
- Not financial advice, and not a recommendation to trade this strategy or to buy any evaluation.
- Futures are leveraged, so you can lose more than you put in.
- The 50K evaluation rules are a typical set that we simulated ourselves. No prop firm made, sponsored or reviewed this.

Found a bug? Open an issue. Want a strategy tested next? Comment on the video.

*Guilty until backtested.*
