# Data pack: "I tested an Instagram strategy exactly as claimed" (EMA9 x VWAP cross)

Episode 1 data pack. Every number in the script and on screen should come from this table or from the JSON files in `data/`. Each number lists its source.

**Source folder (read-only):** `<lab>/strategy-overview/tv/batch14_reel_ema9vwap`. It holds the pre-registered test, run 21 Oct 2026.

**Rebuild:** from `data/build/`, run `python -B build_pack.py`, then `python -B build_stage2.py`, then `python -B build_stage3.py`.
- The `-B` flag stops Python writing bytecode into the read-only source folders.
- Stage 2 reads the local NQ 1-minute parquet only through `local_backtest.load_1m`, which asserts timestamp < 2025-06-01. The holdout is never touched.
- Stage 2 also runs the prop engine.

**Verification:** 365 cross-checks, 0 mismatches (`data/crosscheck.json`).
- Every TradingView row was recomputed from the raw trade lists and checked against `labRes14_export.json`, `results.json`, `results_variants.json` and the REPORT tables: n, PF, net, win %, long/short PF, PF by year, payoff, worst day, days below -$4.5K and trades a session. The X0 + C-REV mirror identity holds, and so do the gross points a trade.
- The local rows were recomputed from the trade CSVs. C-REV, C-LONG and C-RND seed 1 were rebuilt trade by trade and match `local_results.json` to the dollar.
- Both random-side nulls reproduce exactly: TradingView 653 / 782 / 184 and local 37 / 192.
- The May 2025 local trades match the TradingView list trade for trade (72 of 72: entry time, side and $).

**Expected differences, not errors:**
- Max drawdown here is closed-trade (NQ $57,758). TradingView's figure also counts open-trade equity (NQ $58,284). Use TradingView's figure when quoting "max drawdown".
- The case-study prices are the real NQM5 contract. TradingView showed back-adjusted prices exactly +1,506.25 points higher in May 2025. P&L is identical.
- V-ATR NQ payoff is 1.515 exactly. REPORT rounds it to 1.52.
- The NQ tariff trade is 25.7% of the local net. REPORT rounds it to 26%.

## Files

| File | What | Feeds |
|---|---|---|
| `data/claims.json` | Every reel claim, with its quote, timestamp, screen and source; plus our arithmetic on the screens | evidence plane, typed quote cards, claim-vs-reality cards |
| `data/results.json` | Decision rows (NQ, ES, GC), controls, checks (a)-(e), the 1.15 bar, the prior, ES out-of-window, local history, the gold 15m near-miss, the reel window, other timeframes, variants, leads, equity shape | result cards, verdict table, threshold bars |
| `data/equity_NQ.json`, `equity_ES.json`, `equity_GC.json` | Cumulative net by trade on the TradingView window (571 / 594 / 413 points): X0, C-REV, C-RND seeds 1-3, C-LONG and X0-gross. One shared `idx`/`date` axis; max-DD peak and trough kept | equity race (amber X0, white C-LONG benchmark, grey controls) |
| `data/equity_NQ_local.json`, `equity_GC_local.json` | Local 2021-2025 X0 plus C-REV, C-LONG and C-RND seed 1, with the largest trade marked | the "false victory" race |
| `data/equity_ES_OOW.json`, `equity_GC_15m.json` | ES 2023-2025 out of window, and gold 15m with its fade | twist / near-miss scenes |
| `data/mc.json` | Random-side Monte Carlo: `tv_NQ` (the "653") and `local_NQ` (the "37") each have 300 paths, all 1,000 finals and PFs, a 40-bin histogram and the X0 percentile; `tv_ES`, `tv_GC` and `local_GC` have finals and histogram only | MC spaghetti, histogram, percentile readout |
| `data/costs.json` | Gross vs net per market, costs, trades a session, win rate, and the whipsaw mechanism (reversals within N bars, P&L by hold time, chop days) | cost waterfall, mechanism schematic |
| `data/case_trades.json` | Two NQ 3m trades (a winner and a whipsaw loser) with 130 / 103 bars of OHLCV, EMA9, session VWAP and allowed-cross flags, plus every trade of those days | case-study price chart |
| `data/prop.json` | MFFU Pro 50K pass and blow-up odds, size grid, size choice explained, against the reel's 79.9% | prop gauge |
| `data/crosscheck.json` | All 365 checks | audit trail |
| `data/build/*` | Build scripts, prop combos (`prop_combos.json`), raw prop output, stage state | rebuild only |

Colours in the equity files follow the identity: amber `#FFB000` is the strategy, white `#F4F1EA` is the benchmark (always long), grey `#8A93A0` is the other controls, red `#FF5468` is losses.

## Key numbers

All TradingView rows use: 3-minute chart, 1 May 2025 to 1 Oct 2026, 357 New York sessions, 1 contract, $2 a side plus 1 tick slippage. That makes the round trip NQ $14 (0.70 pt), ES $29 (0.58 pt), GC $24 (0.24 pt). "Local" means Databento 1-minute data, 1 Feb 2021 to 30 May 2025.

### The reel's claims (`claims.json`)

| id | value | meaning | source | caveat |
|---|---|---|---|---|
| claim.pf | **1.92** | profit factor on the RoboQuant backtest screen | SPEC "What the reel shows" (frames 00:41-01:08) | read from 360p frames; run is not the template default (card shows 1.84) |
| claim.win | **56.6%** | win rate, 396 trades | same | a bracket profile; the bare cross wins 27-32% |
| claim.trades | **396** trades, 15 Sep 2023 - 24 Sep 2026 | sample on screen | same | about 3.0 years; voice-over says "four-year backtest" (transcript 00:55) |
| claim.prop | **79.9%** | "probability of passing a prop-firm challenge" (simulated: block bootstrap, 1,000 attempts, avg 15.0 calendar days, "Likely to pass") | transcript 00:55 + Prop Firm tab | size not shown; bootstraps a selected curve |
| claim.prop_hist | **78.3%** of 995 rolling 365-day windows | historical pass rate | Prop Firm tab | same |
| claim.prop_dd | **$2,000** trailing EOD drawdown; failures 20.1% | the prop rule the reel used | Prop Firm tab | matches MFFU 50K's drawdown |
| claim.net_B | **+$31,822.54** from $25,000 (+127.29%); max DD -12.3% | config B result | backtest screen | A is exactly 3x B (+$95,467.63, -24.2%) |
| claim.rr | avg R:R **1.47**; avg win **$296.37** / avg loss **-$200.95** (B) | payoff profile | backtest screen | 0.566 x 1.47 / 0.434 = 1.92, internally consistent |
| claim.sharpe | 1.66 (A) / 1.60 (B) | | backtest screen | |
| claim.commission | **$3.00** per round trip | 1,188 / 396 (derived) | SPEC arithmetic | no slippage shown; ours is harsher on purpose |
| claim.card | PF **1.84** / DD **22.0%** / ~+299.9% | the template's own card | frames 01:10-01:16 | blurry; differs from the run shown |
| claim.179k | "$179,000 this past month" | headline P&L | transcript 00:00 | discretionary options P&L, not this backtest |
| claim.hundreds | "automated hundreds of [influencer] strategies ... This is number one." | how it was chosen | transcript 00:47-00:54 | best of many, in-sample; the machine transcript writes "influenza" |
| claim.tps | **0.52** trades a session (396 / ~755 sessions) | template's frequency (derived) | SPEC arithmetic | the rule as voiced trades 3.16-3.40 a session, so the template has hidden filters or a bracket |
| claim.code | code gated behind commenting "ROBOQUANT" | | caption / transcript 01:04 | we did not comment and never saw the code |

### The rule, the bar and the prior

| id | value | meaning | source | caveat |
|---|---|---|---|---|
| rule | EMA(9) of close crosses hlc3 VWAP anchored 09:30 ET; stop-and-reverse; no stop or target; flat 15:57 ET | our reading of the reel | SPEC X0, Pine FNV 2a075770 | template code unseen; [I1]-[I13] interpretation choices |
| bar | **PF >= 1.15** on **n >= 100** | pre-committed pass bar (check a) | SPEC | plus checks (b)-(e) |
| prior | **PF 0.85-1.05** | written before running | SPEC | landed inside on ES (0.857) and NQ (0.940), at the top edge on gold (1.051) |
| checks | (a) PF/n; (b) PF > 1 in 2025 and 2026; (c) beats fade, random seed 1 and always long; (d) local PF > 1; (e) under 1/60 of 1,000 random seeds | the five checks | SPEC, `results.json checks_text` | a variant or other timeframe is never a pass |

### TradingView decision row X0, 3m (`results.json decision_x0_3m`, `equity_*.json`)

| id | value | meaning | source | caveat |
|---|---|---|---|---|
| tv.NQ | **PF 0.940**, 1,128 trades, **-$48,207**, win 30.9%, payoff 2.11 | the reel's rule on NQ | labTrades14 (recomputed) = labRes14 | |
| tv.NQ.years | 2025 **0.914** / 2026 **0.957**; long 0.985 / short 0.897 | | same | |
| tv.NQ.dd | max DD **$58,284** (TradingView) | | labRes14 | closed-trade $57,758 |
| tv.NQ.shape | -$50,348 by 1 Aug 2025 (212 trades, PF 0.589), then **+$57,851** to a peak of **+$7,503** on 25 Nov 2025 (221 trades, **PF 1.474**), then -$55,710 to the end (695 trades, PF 0.900) | equity curve shape | `results.json equity_shape_tv` | the 4-month PF 1.474 stretch is hand-picked; use only to show what a selected window looks like |
| tv.ES | **PF 0.857**, 1,174 trades, **-$59,996**, win 27.4%, payoff 2.27; 2025 0.862 / 2026 0.853 | ES | same | closed-trade equity **never once above $0** in 17 months |
| tv.GC | **PF 1.051**, 1,214 trades, **+$34,184**, win 31.9%, payoff 2.25; 2025 1.139 / 2026 1.014 | gold | same | largest win is 38.8% of net; peak +$41,656 (30 Jan 2026) to -$15,072 (25 Mar 2026) is a -$56,728 drop in 8 weeks |
| tv.tps | **3.16** NQ / **3.29** ES / **3.40** GC trades a session | frequency | n / 357 | vs the template's 0.52 |
| tv.trades_vs_plan | within about 2% of the planning estimate (~1,140 NQ, ~1,190 GC) | the port behaves as planned | REPORT 3 | |

### Controls on the same trades (PF, with net)

| id | X0 | C-REV fade every cross | C-RND seed 1 | seed 2 | seed 3 | C-LONG always long | source |
|---|---|---|---|---|---|---|---|
| ctrl.NQ | 0.940 (-$48,207) | **1.022** (+$16,623) | **0.990** (-$7,877) | 0.899 (-$82,667) | 0.918 (-$66,017) | **1.028** (+$21,233) | labTrades14, all recomputed |
| ctrl.ES | 0.857 (-$59,996) | 0.979 (-$8,096) | 1.017 (+$6,279) | 1.030 (+$11,354) | 1.026 (+$9,779) | 0.948 (-$20,546) | same |
| ctrl.GC | 1.051 (+$34,184) | 0.871 (-$92,456) | 0.923 (-$54,416) | **1.123** (+$78,564) | **1.130** (+$82,724) | 0.890 (-$79,096) | same |

Caveats:
- All controls use X0's exact entry and exit bars, so only the side changes.
- X0 + C-REV = -2 x round trip x n on every market. That is a unit check.
- On NQ and ES all three pre-committed controls beat the rule.
- Gold beats its pre-committed controls, but random seeds 2 and 3 beat gold.

### Random baseline (`mc.json`)

| id | value | meaning | source | caveat |
|---|---|---|---|---|
| mc.tv.NQ | **653 of 1,000** random-side seeds match or beat X0's net (p 0.653) | the rule sits at the **34.7th percentile** of coin flips | results_variants tvNull.NQ; reproduced exactly (numpy default_rng 0..999) | information only; check (e) uses the local history. Raw seeds were not saved, but the run is deterministic and reproduced |
| mc.tv.NQ.pf | random-side PF median **0.977**, 95th pct **1.141** | what luck looks like on these 1,128 windows | same | 39.6% of random seeds end profitable |
| mc.tv.ES | **782 of 1,000** (21.8th percentile) | ES | same | |
| mc.tv.GC | **184 of 1,000** (81.6th percentile); random PF 95th pct **1.123** vs gold's 1.051 | gold is inside chance | same | |
| mc.local.NQ | **37 of 1,000** (p **0.037**; 96.3rd percentile) | long-history NQ beats most coin flips, but not the bar | local_results null.NQ_3m; reproduced | bar was fewer than 1/60, about 16.7 seeds (p < 0.0167, Bonferroni for 3 markets) |
| mc.local.GC | **192 of 1,000** (p 0.192) | | same | |

### Costs and the whipsaw mechanism (`costs.json`)

| id | value | meaning | source | caveat |
|---|---|---|---|---|
| cost.NQ | gross **-$32,415** before costs; costs **$15,792** (1,128 x $14); net -$48,207. Gross **-1.44 pts** a trade vs a 0.70-pt cost | NQ loses **before** costs | labTrades14; matches tvPairs | |
| cost.ES | gross **-$25,950**; costs **$34,046**; net -$59,996; gross -0.44 pt vs 0.58 | ES loses before costs, and costs more than double it | same | |
| cost.GC | gross **+$63,320**; costs **$29,136**; net +$34,184; gross +0.52 pt vs 0.24 | the only market with a gross edge here | same | inside the random band (mc.tv.GC) |
| cost.local | local NQ gross **+2.68 pts** a trade vs 0.70; zero-cost PF NQ 1.105, GC 1.048; at RoboQuant's $3 cost NQ 1.099, GC 1.031 | costs do not explain the gap to 1.92 | REPORT 4 | |
| whip.rev5 | **25.4%** of NQ trades (286) are reversed by the opposite cross within 5 bars (15 min); they win **1.7%** of the time and lose **-$259,184** together | the whipsaw | costs.json NQ whipsaw | ES 26.7% (win 1.0%), GC 26.4% (win 10.9%) |
| whip.long_holds | NQ trades held over 3 hours: 255, win **83.9%**, **+$580,920** | where all the money is made | same | ES +$273,299, GC +$476,556 |
| whip.chop_days | NQ days with 5 or more trades: **89 of 334**, net **-$355,444**, only **3.4%** of them green | chop days | same | hindsight grouping: you only know it was a chop day at the close |
| whip.trend_days | NQ days with exactly 1 trade: 77, net +$249,847 | trend days | same | hindsight grouping |
| whip.payoff | avg winner **$2,162** vs avg loser **-$1,026** (median -$874); 348 winners, 780 losers | big rare wins, many small losses | same | |
| whip.exits | NQ exits: 794 by reversal, 331 at the 15:57 flat, 3 early-close safety exits | | same | median hold 17 bars (51 min) |

### Long history (local data) and out-of-window

| id | value | meaning | source | caveat |
|---|---|---|---|---|
| local.NQ | **PF 1.076**, 3,500 trades, **+$138,540**, win 30.0%, payoff 2.52, max DD $64,537 (closed-trade) | the apparent win | local_results (recomputed from CSV) | fails check (e); by year 1.21 / 1.09 / 0.96 / 1.18 / 0.95 |
| local.NQ.tariff | **one trade**, the 9 Apr 2025 tariff-pause long (entry 12:18 ET), **+$35,636** = **25.7%** of the net; without it PF **1.057** | one day carries it | CSV; REPORT 4 ("26%") | |
| local.NQ.ctrl | fade 0.881, random seed 1 0.916 (seeds 2 and 3: 0.850 and 0.834), always long 1.015 | locally X0 beats every control | local_results | the ordering flips on TradingView |
| local.NQ.recent | last 13 months (May 2024-May 2025) PF 1.088 | | REPORT 4 | |
| local.GC | **PF 0.919**, 3,598 trades, **-$55,942**; p 0.192 | gold long history loses | local_results | fails (d) and (e) |
| local.xcheck | May 2025 overlap: NQ **72 of 72** entries match TradingView, GC **77 of 79** | local engine = TradingView | REPORT 3a | bar was 90% |
| oow.ES | ES 1 May 2023 - 30 Apr 2025: 1,750 trades, **PF 1.053**, +$26,325 (2023 0.941, 2024 1.074, 2025 1.125) | ES before the window | labTrades14 X0-OOW | **one trade (+$21,533, 9 Apr 2025 12:18 ET) is 81.8% of the net**: the same tariff-pause day that carries NQ locally |

### Leads, near-misses and reconstructions

| id | value | meaning | source | caveat |
|---|---|---|---|---|
| lead.GC15 | gold 15m X0 **PF 1.204**, 440 trades, +$53,870; fade **0.771**; 2025 1.171 / 2026 1.223 | the one combo that clears the numeric bar | labTrades14 X0-tf / C-REV-tf (recomputed) | not the decision row; best of 86; local gold 15m 2021-2025 is **PF 0.857** (1,382 trades, p 0.709) |
| lead.V1D | first cross of the day only: NQ 3m **PF 1.215** (334 trades); NQ 1m **1.540** (350); NQ 5m 1.316 (321) | best-of-86 picks look great | results_variants leads | selection bias; local NQ 3m version is 0.91 in 2023 and 0.68 in Jan-May 2025 |
| reelwin | the reel's own dates (15 Sep 2023 - 24 Sep 2026): NQ **1.032** (2,425 trades), ES **0.972** (2,556), GC **1.020** (2,577) | none is near 1.92 | results_variants reelWindow | NQ and GC mix local + TradingView data |
| vatr | bracket copy (1 ATR stop, 1.5R target): PF NQ **1.010** / ES **0.792** / GC **0.980**; win 40.0% / 35.9% / 40.0%; payoff 1.515 / 1.416 / 1.473 | gets the reel's 1.47 payoff, not its 56.6% wins | labTrades14 V-ATR | our bracket numbers, not fitted |
| other_tf | X0 on 1 / 2 / 3 / 5 / 15m: NQ 0.968 / 0.996 / 0.940 / 0.965 / 1.010; ES 0.896 / 0.919 / 0.857 / 0.929 / 0.901; GC 1.000 / 1.000 / 1.051 / 0.955 / 1.204 | no timeframe rescues it | results.json other_timeframes_tv | |

### Prop odds (`prop.json`)

| id | value | meaning | source | caveat |
|---|---|---|---|---|
| prop.reel | **79.9%** pass | the claim | claims.json | |
| prop.tv.1mnq | **15.3% pass / 84.7% blow-up**, median 32 trading days to pass | the rule's NQ trades on MFFU Pro 50K ($3,000 target, $2,000 EOD trailing, 50% consistency) at **1 MNQ** | prop_mc.cjs, 5,000 sims, seed 20261001, 5-day blocks | **upper bound**: MAE is not in the TradingView export, so intraday drawdown inside a trade is not counted |
| prop.tv.1nq | **14.7% pass / 85.3% blow-up**, median 4 days | at 1 NQ mini | same | same |
| prop.tv.best | best of 12 sizes: **5 MNQ, 16.8%** | | same | |
| prop.local.1mnq | **31.1% pass / 68.8% blow-up** (median 59 days); 1 mini 13.8% | long history with MAE from 1-minute bars | same engine on local trades | the history that still had a gross edge |
| prop.size | 1 MNQ is the headline size | rule at 1 micro wins about $215 and loses about $104 a trade; reel run B wins $296 and loses $201; at 1 mini the rule wins $2,162 and loses $1,026 | prop.json size_choice | the reel's size is unknown |
| risk.NQ | worst trade **-$8,299** (11 Jun 2026); worst day **-$12,523** (18 Dec 2025); **85 of 334** days lost more than $2,000 at 1 mini; 41 lost more than $4,500 | why a no-stop rule fails a $2,000 drawdown | labTrades14 (= results.json) | at 1 micro about -$830 / -$1,252 |

### Case trades (`case_trades.json`, local NQM5 bars; May 2025 is inside the TradingView window)

| id | value | meaning | source | caveat |
|---|---|---|---|---|
| case.win | **13 May 2025**: long 09:45 -> 15:57 flat, **+217.25 pts, +$4,341**, held 124 bars (6 h 12 min). Signal bar 09:42: EMA 21,042.70 vs VWAP 21,042.57. The day's first trade, a short at 09:36, lost $109 | the move the reel shows | local engine (matches TradingView 72/72) | best NQ trade of May (2.0x the average winner): a best case, not a typical one |
| case.whip | **20 May 2025**: **7 trades, all 7 losers, day -$5,308**. Featured: short 10:33 -> 10:39 (2 bars), **-36.75 pts, -$739**. The first trade (short 09:51) lasted one bar, -$1,109 | a typical whipsaw | same | featured = the short-hold loser closest to the median NQ loser (-$874) |
| case.prices | NQM5 21,067.00 -> 21,284.25 (winner) | real contract prices | Databento | TradingView showed +1,506.25 pts (B-ADJ back-adjusted) |

## Arc candidates

The benchmark asks for at least 3 runs, 1 false victory, 1 control and 1 random baseline. These sequences are all true to the test. A is the recommended spine.

**A. The real lab-notebook order (recommended).** This is how the test actually happened: the local-only verdict came first, then the TradingView run (REPORT_before_reel14tv.md, then REPORT.md).
1. **Run 1, as claimed, on four years of NQ (local, 2021-2025): the false victory.** PF 1.076 and +$138,540 on 3,500 trades. It beats the fade (0.881), the random side (0.916) and always long (1.015). "This should work, right?"
2. **Twist.** One trade, the 9 Apr 2025 tariff-pause long (+$35,636), is 26% of all the profit; without it the PF is 1.057. The random baseline: 37 of 1,000 coin-flip versions earn as much (p 0.037). The pre-committed bar was fewer than 17.
3. **Run 2, fresh data our first run never saw (TradingView, May 2025 - Oct 2026).** Not "a window the reel never showed": the reel's chart (15 Sep 2023 - 24 Sep 2026) overlaps it.
   - NQ falls to 0.940 (-$48,207).
   - Control: fading every cross (1.022) and buying every time (1.028) both beat it.
   - Random: 653 of 1,000 coin flips match it.
4. **Run 3, the survivor that isn't.**
   - Gold is up +$34,184 (PF 1.051) and beats all three pre-committed controls. That is false victory number 2.
   - Then random seeds 2 and 3 score 1.123 and 1.130, 184 of 1,000 coin flips match it, it is below the 1.15 bar, and long-history gold is 0.919.
   - ES never once goes above zero.
5. **Run 4, rebuild the reel's profile.**
   - Adding a bracket gets the 1.47 payoff, but wins only 36-40%, not 56.6% (PF 1.010 / 0.792 / 0.980).
   - On the reel's own dates the bare rule makes NQ 1.032, ES 0.972 and gold 1.020.
6. **Prop and verdict.** The reel claims 79.9%. The rule's own trades pass 15.3% and blow up 84.7% at 1 MNQ, and that is an upper bound. Verdict: no.

**B. "We did what the reel did" (selection-bias twist for B8).**
- The test ran 86 combos. The best of them look as good as the reel: first cross of the day on NQ 1m is PF 1.540, and gold 15m is 1.204.
- The reel says it is the best of "hundreds". Callback: "best of many" is exactly what produces a 1.92.
- The honest kill: gold 15m is 0.857 on four years of local data, and NQ's best-of-86 lead (first cross, 3m) is 0.91 in 2023 and 0.68 in 2025 locally.
- Strong as the B8 twist inside arc A.

**C. Market by market.** NQ fails, ES is worse (never profitable), gold is the false victory, the random baseline kills gold, and the gold 15m near-miss is killed by local data. Simpler, but it loses the "four years looked great" hook.

**D. Inside one equity curve (for the B4/B7 race, honest only if labelled).** The NQ TradingView curve is -$50,348 by 1 Aug 2025. It then rallies +$57,851 in four months (PF 1.474) to +$7,503 on 25 Nov 2025, then gives it all back. Use this to show how a hand-picked window becomes a "1.47 PF strategy". Always say it is hand-picked.

**Open-loop candidates.**
- Long loop: "the reel says 79.9% pass. What does the rule's own data say?" Pay off at the prop gauge.
- Short loop: "why does a rule with 2x bigger winners than losers lose money?" Pay off with the whipsaw stats.
- Sponsor bridge: none, because there is no sponsor. Use a code-offer slot or skip it.

## Real confession material (only what actually happened)

1. **We wrote a verdict before the main test ran.** The first TradingView run never happened: the agent could not open a browser (tabs_create and navigate refused), so the first report was written from local data only and says "TradingView has not run" (workflow_summary.txt, REPORT_before_reel14tv.md). All 86 combos ran later the same day. The verdict did not change.
2. **A real bug in our own Pine code.**
   - The code audit found that a cross on the last bar of an early-close session, taken while flat, would fill at the next Globex open (line 489 lacks `not session.islastbar`).
   - It did not trigger: 0 overnight entries locally, and in TradingView every entry was inside 09:30-16:00 ET with a same-day exit. The window's early-close days were 2025-07-03, 2025-11-28 and 2025-12-24.
   - The fix is still not applied to the Pine file (audit.json, REPORT 10).
3. **We misread a number off the reel.** SPEC quotes config A's commission as -$3,554. But 3 x $1,188 is $3,564, so it was probably a frame misread at 360p (verification checker, workflow_summary.txt). Nothing used it.
4. **Our report had wrong sentences that the checker caught.**
   - A sentence said none of the leads reaches PF 1.15, but NQ first-cross-only was 1.242 locally.
   - Gold's cost was written as "2.4 pts" instead of 0.24.
   - An early-close flat time of "13:12" was a bar open, not the fill (workflow_summary.txt).
5. **The task text we were given had the data overlap backwards.** It said ES/GC overlap and NQ doesn't; it is NQ/GC, and ES has no local data (workflow_summary.txt).
6. **The run wiped another strategy off the lab chart.** Loading our script removed the study that was on the Strategy Lab chart (TM 50% Fib Strategy v2.5) (REPORT 3).
7. **Light, self-deprecating option.** Our own transcription tool heard "influencer strategies" as "influenza strategies" (transcript_local.txt). The joke is on the tool, never the creator.

## Gaps and caveats

- **Prop odds on the TradingView window are an upper bound.** The TradingView export has no per-trade MAE, so intraday drawdown inside a trade is not counted. The local run counts it (31.1% at 1 MNQ on the long history).
- **ES has no local data**, so checks (d) and (e) cannot run on ES.
- **Case-study bars exist only up to 30 May 2025.** The holdout rule forbids local data after 2025-06-01, and no TradingView bars were saved. Both case trades are from May 2025, so they are inside the TradingView window and verified against it.
- **The reel's market, size and code are unknown.** The template code was gated (comment "ROBOQUANT") and was never seen. We test the rule as voiced, not the template.
- **The reel quotes come from a machine transcript** (faster-whisper, 360p copy) and were not verified word for word. Re-listen before typing any quote on screen.
- **Max DD:** our curves are closed-trade; TradingView's figures include open equity. Quote TradingView's.
- **Mixed sources:** the reel-window figures mix local and TradingView data. They agree on the May 2025 overlap.
- **Hindsight groupings:** the "chop days" and "trend days" stats group days by how many trades they had, which you only know at the close. They explain the mechanism; they are not a filter.
- **No viewer comments exist** (new channel), so the community screens need placeholders or must be cut. Never invent comments.
- **Reel footage** is third-party. The data pack contains no frames; using clips is a fair-use call for the user.
