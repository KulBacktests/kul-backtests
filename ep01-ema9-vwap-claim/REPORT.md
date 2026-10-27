## EMA9 x VWAP cross (Tim Hutter reel / RoboQuant): does it hold up?
Report for the user's question about the Instagram reel ("Can you make and run this strat? see if it holds up"). First written on 21 Oct 2026 from local data only; updated the same afternoon with the TradingView rows (all 86 planned combos ran). The previous version is REPORT_before_reel14tv.md.

### Verdict
**It does not hold up, on any market, in TradingView or on local data.** The rule as the reel describes it fails the pre-committed test on NQ, ES and gold. The rule: 3-minute chart, EMA(9) of close crossing the hlc3 VWAP anchored at 09:30 ET, stop-and-reverse, no stop or target, flat at 15:59 ET (the MFFU rule).

TradingView, 1 May 2025 to 1 Oct 2026, decision row X0 on 3m (bar: n >= 100 and PF >= 1.15):
- **NQ:** PF 0.940 on 1,128 trades, -$48,207 (2025 0.914, 2026 0.957). Fading every cross (1.022), a random side (0.990) and always long (1.028) all do better.
- **ES:** PF 0.857 on 1,174 trades, -$59,996 (2025 0.862, 2026 0.853). Fade 0.979, random 1.017 and always long 0.948 all do better.
- **Gold:** PF 1.051 on 1,214 trades, +$34,184 (2025 1.139, 2026 1.014). It beats fade (0.871), random seed 1 (0.923) and always long (0.890), but random seeds 2 and 3 score 1.123 and 1.130, and it is below the 1.15 bar.

Local data, 1 Feb 2021 to 30 May 2025 (unchanged):
- **NQ 3m:** PF 1.076 on 3,500 trades, but 37 of 1,000 random-side seeds earn at least as much (p 0.037, bar 1/60 = 0.017).
- **Gold 3m:** PF 0.919 on 3,598 trades, p 0.192.

Per market, the first check that fails is (a), the TradingView PF bar:
- **NQ** fails (a), (b), (c) and (e).
- **ES** fails (a), (b) and (c), so it does not even reach "holds up on TradingView only (provisional)".
- **Gold** fails (a), (d) and (e).

**Payout Odds is unchanged.** One default combo meets the numeric bar: gold 15m X0, PF 1.204 on 440 trades, fade 0.771. But it is not the decision row, the overall verdict does not allow it, and local gold 15m is 0.857.

### 1. Reel claims (data, not trusted)
- **Source:** Tim Hutter (@timhutter.official), posted 18 Oct 2026: "EMA 9 + VWAP, automated". The strategy is RoboQuant's template "Daily Anchored VWAP Signal Strategy". Its code is only given to people who comment "ROBOQUANT"; we did not, so it was not seen.
- **Backtest screen:** 396 trades from 15 Sep 2023 to 24 Sep 2026 (about 3 years, not the 4 in the voice-over). 56.6% winners, PF 1.92, Sharpe 1.66, average R:R 1.47.
- **Size B:** +$31,822.54 from $25K, max DD -12.3%, $3.00 commission per round trip. Size A is exactly 3x B.
- **Prop tab:** 79.9% simulated pass and 78.3% of 995 rolling 365-day windows, on a $2,000 trailing EOD drawdown.
- **Template card:** PF 1.84 / DD 22.0%, so the run shown is not the template's default.
- **"$179K last month":** discretionary options P&L, not this backtest.

### 2. What was tested
- **Rules and pre-registration:** SPEC.md and TEST_PLAN.json were pre-registered. The Pine file is Desktop\Pine Strats\EMA9 x VWAP Cross 3m (reel test, trade boxes).pine, byte-identical to src\rl-ema9-vwap-cross.pine (FNV 2a075770). It compiles clean, and calc_on_order_fills, calc_on_every_tick and process_orders_on_close are all off.
- **Costs:** 1 contract, $2 per side, 1 tick slippage. Round trip: NQ $14, ES $29, GC $24.
- **Local data:** Databento GLBX 1-minute unadjusted front month, NQ and GC. Every read used timestamp < 2025-06-01 UTC, asserted; the last bar is 2025-05-30 20:59 UTC, so the holdout was not touched. 1,088 NY sessions per market.
- **Port check:** cross counts match the independent plan_counts.py on all 20 cells.
- **Controls, on the same trades:** C-REV fades every cross, C-RND picks a random side, C-LONG is always long.
- **Prior written before the run:** PF 0.85-1.05. TradingView landed inside it on ES and NQ, and at its top edge on gold (0.857 / 0.940 / 1.051).

### 3. TradingView window, 1 May 2025 to 1 Oct 2026
**How it ran (lab_rows.json, labRes14_export.json, labTrades14_export.json)**
- Follow-up lab run on 21 Oct 2026, about 13:00-13:50 UTC, in its own built-in-browser tab. Tab "seed" was not touched, and the tab was closed at the end.
- Layout: Strategy Lab, a private TradingView layout only.
- Source: src/rl-ema9-vwap-cross.pine (FNV 2a075770, 34,041 characters, 599 editor lines), loaded into the UNSAVED Untitled Pine tab and added with "Add to chart" only. Nothing was saved or published, and there were no alerts and no orders.
- The runner's load removed the study that was on that chart before (TM 50% Fib Strategy v2.5). At the end, the reel study was left on the chart on GC 15m with the last row's inputs (V-1D). The script is unsaved.
- **B-ADJ state: ON.** When the layout opened, "Adjust for contract changes" was active (aria-pressed=true). It was not changed. It does not matter for this rule, which only compares two values of the same series.
- Strategy properties were read back from the study: 1 contract, $2/side, 1 tick, $150K, margin 0, bar magnifier on, COF / every tick / on close off, pyramiding 0.
- Deep Backtesting range: 2025-05-01 to 2026-10-01. Every row's btFrom equals the wanted start. X0-OOW ran 2023-05-01 to 2025-05-01. Afterwards the range was set back, and X0 NQ 3m re-read identically (1,128 / -$48,207 / 0.9398).
- **All 86 planned combos returned "ok"** (P1 12, P2 36, P3 38), at about 12 s each.

**Decision row X0, 3m**

| | n | PF | net | win | payoff | 2025 / 2026 | long / short PF | max DD | trades a session |
|---|---|---|---|---|---|---|---|---|---|
| NQ | 1,128 | 0.940 | -$48,207 | 30.9% | 2.11 | 0.914 / 0.957 | 0.985 / 0.897 | $58,284 | 3.16 |
| ES | 1,174 | 0.857 | -$59,996 | 27.4% | 2.27 | 0.862 / 0.853 | 0.887 / 0.827 | $62,566 | 3.29 |
| GC | 1,214 | 1.051 | +$34,184 | 31.9% | 2.25 | 1.139 / 1.014 | 0.977 / 1.131 | $58,870 | 3.40 |

- GC's largest win is 38.8% of its net.
- Trade counts are about 2% of the planning estimate (about 1,140 NQ and 1,190 GC).
- Trades a session = n / 357 New York sessions.

**Controls on the same chart, 3m (PF)**

| | X0 | C-REV (fade) | C-RND seed 1 | seed 2 | seed 3 | C-LONG |
|---|---|---|---|---|---|---|
| NQ | 0.940 | 1.022 | 0.990 | 0.899 | 0.918 | 1.028 |
| ES | 0.857 | 0.979 | 1.017 | 1.030 | 1.026 | 0.948 |
| GC | 1.051 | 0.871 | 0.923 | 1.123 | 1.130 | 0.890 |

**Gross edge before costs**, from the X0 / C-REV pairs: (net X0 - net C-REV) / 2 / n.
- **3m:** NQ -1.44 points a trade, ES -0.44, GC +0.52. Cost per trade is exactly $14 / $29 / $24.
- **Other timeframes:** NQ -0.70 to +1.10 points, ES -0.20 to +0.07, GC -0.05 to +1.46 (15m).
- On NQ and ES the cross has no gross edge in this window. On gold 3m it covers about twice the 0.24-point round trip.

**Random-side check on the TradingView trades** (information only; the pre-committed check (e) uses the local history):
- Method: 1,000 seeds, using the same formula as the local null. It reproduces C-REV trade by trade to the cent.
- Seeds that reach X0's net: NQ 653 (p 0.653), ES 782 (p 0.782), GC 184 (p 0.184).
- The random-side PF has a 95th percentile of 1.141 (NQ), 1.056 (ES) and 1.123 (GC). So gold's 1.051 is well inside chance.

**Other timeframes, X0 (default inputs; on the page), with the fade on the same chart**

| | 1m | 2m | 3m | 5m | 15m |
|---|---|---|---|---|---|
| NQ X0 (n) | 0.968 (1,929) | 0.996 (1,366) | 0.940 (1,128) | 0.965 (826) | 1.010 (480) |
| NQ fade | 0.979 | 0.960 | 1.022 | 1.000 | 0.957 |
| ES X0 (n) | 0.896 (2,038) | 0.919 (1,410) | 0.857 (1,174) | 0.929 (882) | 0.901 (503) |
| ES fade | 0.874 | 0.895 | 0.979 | 0.915 | 0.950 |
| GC X0 (n) | 1.000 (2,229) | 1.000 (1,576) | 1.051 (1,214) | 0.955 (912) | 1.204 (440) |
| GC fade | 0.881 | 0.903 | 0.871 | 0.969 | 0.771 |

- **Gold 15m:** 1.171 in 2025 and 1.223 in 2026. Long PF 1.029 (230 trades), short 1.425 (210); the largest win is 27.7% of the net. Local gold 15m is 0.857 on 1,382 trades (p 0.709), so the long history contradicts it.
- **NQ 15m:** 1.010, made of 0.782 in 2025 and 1.144 in 2026.

**Variants and controls on 3m (PF; NQ / ES / GC)**
- **V-ATR (1 ATR stop, 1.5R target):** 1.010 / 0.792 / 0.980. Win rate 40.0% / 35.9% / 40.0%, payoff 1.52 / 1.42 / 1.47. Its fade, C-REV-ATR: 0.895 / 0.888 / 0.887.
- **V-1D (first cross of the day only):** 1.215 (334 trades; 2025 1.018, 2026 1.333) / 0.895 / 1.042.
- **V-1D-ATR:** 1.132 / 0.680 / 1.042.
- **V-NY15 (entries until 15:00):** 0.945 / 0.867 / 1.058.
- **V-GX (Globex 18:00 VWAP, RTH entries):** 0.898 / 0.801 / 0.913.
- **V-GX24 (Globex VWAP, entries 18:00-15:5x):** 1.014 / 0.802 / 1.157 (2,594 trades). It carries overnight risk: 59 gold days below -$4.5K.
- **V-MID (00:00 VWAP):** 0.931 / 0.835 / 1.045.
- **V-GC0820 (gold 08:20 VWAP):** 0.919.

**Priority-3 rows on other timeframes**
- **C-REV:** NQ 0.957-1.000, ES 0.874-0.950, GC 0.771-0.969.
- **V-ATR, on 1 / 5 / 15m:** NQ 0.964 / 1.000 / 1.082, ES 0.783 / 0.892 / 0.930, GC 0.938 / 0.874 / 0.958.
- **V-1D, on 1 / 5 / 15m:**
  - NQ 1.540 (350 trades; 2025 1.102, 2026 1.827) / 1.316 (321) / 1.070;
  - ES 0.904 / 1.034 / 1.029;
  - GC 0.870 / 0.750 / 1.238 (251).

**ES out of window (X0-OOW), 3m, 1 May 2023 to 30 Apr 2025.** Deep Backtesting reached that far.
- 1,750 trades, PF 1.053, +$26,325. By year: 2023 0.941, 2024 1.074, 2025 (Jan-Apr) 1.125.
- One trade (+$21,533 in April 2025) is 81.8% of the net, so the result rests on that single trade.

**Unit checks (all pass)**
- C-RND (seeds 1-3), C-LONG, V-ATR and C-REV-ATR have X0's trade count on every 3m market (1,128 / 1,174 / 1,214), and V-1D-ATR has V-1D's.
- X0 net + C-REV net = -2 x round trip x n on every market and timeframe. For 3m: NQ -31,584, ES -68,092, GC -58,272.
- Every NY-anchored row enters inside 09:30-16:00 ET and exits on the same New York date. The audit's early-close bug did not trigger.

### 3a. Cross-check, May 2025 (X0 3m, TradingView against the local engine)
Command: `python local_backtest.py --xcheck NQ|GC labTrades14_export.json`. Output is in driver\xcheck_NQ.txt and driver\xcheck_GC.txt.

The bar (SPEC) was that at least 90% of entries match in time and side.
- **NQ:** 72 local / 72 TradingView trades. All 72 match (100%), every exit is on the same bar, and the mean $ difference is 0.00. **Pass.**
- **GC:** 79 / 79 trades. 77 match (97.5%), 76 exits are on the same bar, and the mean $ difference is -0.26. **Pass.**
- **The 2 GC mismatches** are both on 2025-05-28: local 14:30 L and 15:15 S, against TradingView 14:54 L and 15:09 S.
- **Conclusion:** the local engine reproduces TradingView, so the local 2021-2025 numbers can be trusted.
- The run added its result to local_results.json under "xcheck" and left the rest of the file unchanged (backup: driver\local_results.before_xcheck.json). The "status" text inside that block still says "pending"; results_variants.json carries the corrected status.

### 4. Local X0 results, 2021-02 to 2025-05
Columns: n, PF, net, win rate. Then PF by year 2021 / 2022 / 2023 / 2024 / 2025 (Jan-May), then p random.

**NQ**
- 1m: 6,192 trades, PF 1.104, +$243,997, win 24.2%. By year 1.14 / 1.13 / 1.05 / 1.13 / 1.06. p 0.001.
- 2m: 4,333 trades, PF 1.116, +$235,843, win 27.9%. By year 1.22 / 1.11 / 1.01 / 1.20 / 1.04. p 0.004.
- **3m: 3,500 trades, PF 1.076, +$138,540, win 30.0%, payoff 2.52, max DD $64.5K (closed-trade).** By year 1.21 / 1.09 / 0.96 / 1.18 / 0.95. p 0.037.
- 5m: 2,744 trades, PF 1.071, +$113,314. By year 1.25 / 1.12 / 0.96 / 1.16 / 0.86. p 0.065.
- 15m: 1,395 trades, PF 1.142, +$120,860, win 44.2%. By year 1.33 / 1.08 / 1.10 / 1.17 / 1.13. p 0.026.

**GC**
- 1m: PF 0.900 (p 0.054).
- 2m: PF 0.892 (p 0.241).
- **3m: 3,598 trades, PF 0.919, -$55,942.** By year 0.79 / 1.05 / 0.96 / 0.94 / 0.83. p 0.192.
- 5m: PF 0.997 (p 0.016).
- 15m: PF 0.857 (p 0.709).

**Gross edge before costs**
- NQ: 2.7-5.0 points per trade, against a 0.70-point round-trip cost.
- GC: about 0.085 points per trade, against a 0.24-point cost.

**What sits behind the NQ 3m number**
- One trade, the 2025-04-09 tariff-pause long (+$35,636), is 26% of the net. Without it, PF is 1.057.
- Long trades PF 1.120, short trades 1.034.
- Latest 13 months (May 2024 to May 2025): NQ 1.088, GC 0.865.

**Local against TradingView.** NQ goes from 1.076 locally to 0.940 in TradingView. Gold goes from 0.919 to 1.051. Over both periods neither market keeps an edge, and gold's TradingView gain sits inside its own random-side band.

**Costs do not explain the gap:**
- At RoboQuant's $3 round trip with no slippage: NQ 1.099, GC 1.031.
- At zero cost: NQ 1.105, GC 1.048.

### 5. Local controls (PF: X0 / fade / random seed 1 / always long; then random seeds of 1,000 that reach X0's net)
**NQ**
- 1m: 1.104 / 0.841 / 0.915 / 0.990; 1 seed.
- 2m: 1.116 / 0.845 / 0.972 / 0.991; 4 seeds.
- **3m: 1.076 / 0.881 / 0.916 (seed 2: 0.850, seed 3: 0.834) / 1.015; 37 seeds.**
- 5m: 1.071 / 0.891 / 1.019 / 1.025; 65 seeds.
- 15m: 1.142 / 0.839 / 0.910 / 1.053; 26 seeds.

**GC**
- **3m: 0.919 / 0.830 / 0.879 (seed 2: 0.905, seed 3: 0.902) / 0.966; 192 seeds.**
- 5m: 0.997, with 16 seeds.
- 15m: 0.857 / 0.927 / 0.812 / 0.947.

Locally on NQ, X0 beats all three controls on every timeframe, but on 3m it does not beat chance at the pre-committed strictness. In TradingView the NQ ordering flips: the fade, the random side and always long all beat X0. On every row, local and TradingView, X0 net + fade net = -2 x n x round trip, exactly.

### 6. Local variants on 3m (leads only)
- **ATR bracket (1 ATR(14) stop, 1.5R target):** NQ 0.918, GC 0.910. It reproduces the reel's 1.47 payoff, but wins only 38.5% / 38.0%, against the reel's 56.6%. Faded, it is 0.908 / 0.786.
- **One trade a day:** NQ 1.242 (by year 1.33 / 1.30 / 0.91 / 1.90 / 0.68), GC 0.868.
- **One trade a day with the bracket:** 1.038 / 0.934.
- **Entries until 15:00:** 1.085 / 0.924.
- **Globex 18:00 VWAP:** 1.009 / 0.954.
- **Midnight VWAP:** 1.036 / 0.894.
- **Gold 08:20 VWAP:** 0.927.

### 7. Pre-committed check
The five checks (SPEC.md):
- (a) TradingView: n >= 100 and PF >= 1.15.
- (b) PF above 1 in 2025 and in 2026.
- (c) X0 beats C-REV, C-RND (seed 1) and C-LONG on the same chart.
- (d) Local PF above 1.
- (e) Fewer than 1/60 of 1,000 random seeds reach X0's local net.

| | (a) n, PF | (b) 2025 / 2026 | (c) controls | (d) local PF | (e) local p | result |
|---|---|---|---|---|---|---|
| NQ | 1,128, 0.940: **fail** | 0.914 / 0.957: **fail** | below all three: **fail** | 1.076: pass | 0.037: **fail** | **fails** |
| ES | 1,174, 0.857: **fail** | 0.862 / 0.853: **fail** | below all three: **fail** | no local data | no local data | **fails** (not even provisional) |
| GC | 1,214, 1.051: **fail** | 1.139 / 1.014: pass | above all three: pass | 0.919: **fail** | 0.192: **fail** | **fails** |

- **ES:** the provisional label needs (a)-(c) plus PF > 1 on X0-OOW. X0-OOW is 1.053, but (a)-(c) fail, and 81.8% of the X0-OOW net is one trade.
- **GC (c):** it passes against seed 1, the pre-committed control, but random seeds 2 and 3 on the same chart score 1.123 and 1.130.

**Overall: DOES NOT HOLD UP.** The first failed check is (a) on all three markets.

**Leads only** (SPEC: another timeframe or a variant is never a pass). Each would need its own pre-registered test, local data first. All are best-of-86 picks, so they carry selection bias.
- **V-1D, first cross of the day only, on NQ:**
  - 1m: PF 1.540 on 350 trades (2025 1.102, 2026 1.827).
  - 5m: 1.316 on 321.
  - 3m: 1.215 on 334. Locally the 3m version is 1.242, but 0.91 in 2023 and 0.68 in Jan-May 2025.
- **X0 gold 15m:** 1.204 on 440 trades (fade 0.771). Local gold 15m is 0.857.
- **V-1D gold 15m:** 1.238 on 251 trades.
- **V-GX24 gold 3m:** 1.157 on 2,594 trades, with overnight risk.
- **Earlier local leads:** NQ 1m, 2m and 15m X0 (PF 1.10-1.14, above 1 every year). In TradingView they are 0.968, 0.996 and 1.010, so they do not survive.

### 8. Why our result differs from RoboQuant's PF 1.92 and 79.9% pass
1. **On the reel's own dates the rule has no edge.** For 15 Sep 2023 to 24 Sep 2026, X0 3m is:
   - **NQ PF 1.032** on 2,425 trades: local to April 2025 (1.107), then TradingView (0.961);
   - **ES 0.972** on 2,556: TradingView X0-OOW to April 2025 (1.082), then TradingView X0 (0.858);
   - **gold 1.020** on 2,577: local 0.948, then TradingView 1.053.

   None is near 1.92 (results_variants.json "reelWindow"; the NQ and gold figures mix two sources, which agree on the May 2025 overlap).
2. **It is a different strategy.** The template trades 0.52 times a session; the rule in the voice-over trades 3.2-3.4 times in TradingView. A 56.6% win rate with a 1.47 payoff is a bracket profile, not stop-and-reverse (X0 wins 27-32%). So the template has hidden filters or a bracket.
3. **Our bracket copy does not get there either.** V-ATR has the reel's payoff (1.42-1.52 in TradingView) but wins 36-40%, and its PF is 1.010 / 0.792 / 0.980.
4. **The run is a selected configuration, not the default.** The card says 1.84 / 22.0% and the run 1.92 / 24.2%. The presenter says he automated "hundreds" of strategies, so this is the best of many, in-sample.
5. **Not costs:** even at zero cost the local rule is only NQ 1.105 / GC 1.048. In TradingView, NQ and ES lose before costs.
6. **The 79.9% pass rate** bootstraps that selected curve on a $2,000 trailing drawdown at an unknown size. The bare rule has no stop:
   - in TradingView, 41 of its 334 NQ trading days lost more than the MFFU $4.5K trailing drawdown at 1 mini;
   - with negative expectancy on NQ and ES, a prop simulation would only measure how fast it fails;
   - no Monte Carlo was run because the verdict is a fail (SPEC).
7. **The $179K headline** is options trading, not this backtest.

### 9. Prop risk (MFFU Pro 150K: $4.5K trailing drawdown)
The 1-micro figures are 1/10 of the mini figures. At micro size the $2/side commission eats a much larger share of each trade.

**TradingView, X0 3m, 1 mini**

| | worst trade | worst day | days below -$4.5K |
|---|---|---|---|
| NQ | -$8,299 (2026-06-11) | -$12,523 (2025-12-18) | 41 of 334 trading days |
| ES | -$3,117 | -$8,016 (2026-06-25) | 10 of 330 |
| GC | -$10,694 (2026-02-12) | -$11,602 (2026-01-21) | 19 of 341 |

- NQ at 1 micro: about -$830 worst trade and -$1,252 worst day.
- Gold 5m X0 had a -$31,640 day on 2026-01-29 at 1 mini.

**Local, 1 mini**
- **NQ 3m:** worst trade -$6,994 and worst day -$20,879, both on 2025-04-07. 60 of 1,005 trading days were below -$4,500. At 1 micro that is about -$699 and -$2,088.
- **GC 3m:** worst trade -$2,674, worst day -$6,650 (2025-04-09).

### 10. Code audit (audit.json, verdict "minor issue (no look-ahead)"), word for word
"Code checked 21 Oct 2026: no look-ahead. Signals use confirmed bar closes (EMA9 and a 09:30-anchored hlc3 VWAP of the same series) and fill at the next open; calc_on_order_fills, calc_on_every_tick and process_orders_on_close are off; there is no request.security; brackets are placed with the entry; the trade boxes only draw; and nothing compares price levels, so B-ADJ does not matter. One minor bug: a cross on the last bar of an early-close session, taken while flat, sends an entry that fills at the next Globex open, and the safety exit closes it one bar later. The fix is to add 'not session.islastbar' to the cross gate at line 489. It can touch at most 3 TradingView-window days (2025-07-03, 2025-11-28, 2025-12-24)."

The back-adjustment and look-ahead rules are both satisfied.
- The bug did not trigger locally: 0 overnight entries on the NY-anchored rows.
- It did not trigger in TradingView either: every NY-anchored row enters 09:30-16:00 ET and exits the same date.
- The fix is still not applied to the Pine file.

### 11. Dashboards
**Strategy Lab Results** (files only, not republished):
- **Family "reel" ("Social-media reels")** with one strategy: id rl-ema9-vwap-cross, label "EMA9 x VWAP Cross (reel: Tim Hutter / RoboQuant) [reel]".
- **15 TradingView default rows** (NQ/ES/GC x 1/2/3/5/15m) now carry real numbers (status "ok") instead of "not run".
- **10 local X0 rows** (NQ/GC x 5 timeframes) are unchanged.
- **Notes:** the TradingView note (REEL14_NOTE in build_data.py) was rewritten by patch_build_data_reel14tv.py. It now has the TradingView results, the controls, the gross edge, the other timeframes, ES out of window, the cross-check, the local history, the final verdict, the reel-window comparison, the bracket copy, the leads and the prop risk, and it still ends with the audit line word for word (asserted). The local note's last sentence now gives the TradingView result instead of "not run yet".
- **Variants and controls** are in results_variants.json (tvOther, tvPairs, tvNull, reelWindow, leads, verdict), which the page does not read.
- **Takeaway:** the reel line at the top of ul#takeaways was replaced by patch_takeaway_reel14tv.py. Nothing outside that `<ul>` changed (asserted).

**Rebuild check** (python build_data.py tv/tv_export_latest.txt tv/decl_export.json):
- Before patching, a rebuild reproduced the old data.json exactly (except the generated time).
- After the patch:
  - 209 strategies and 2,947 rows, in the same order.
  - The only changed rows are the 15 reel TradingView rows ("not run" -> "ok" with results). The 10 reel local rows and all 2,922 other rows are identical.
  - The only changed strategy fields are the reel's tvNote and localNote.
  - Meta: tvDone 203 -> 204 (the reel strategy now counts as done), tvTotal 209, and the generated time.
  - tv_results.json and community_meta.json have the same MD5 as before.
- Backups (*_before_reel14tv.*):
  - build_data.py, overview/data.json, overview/index.html, tv/tv_results.json, tv/community_meta.json;
  - in this folder: make_results.py, results.json, results_variants.json, leaders.json, local_rows.json, REPORT.md.

**Payout Odds: does not qualify, nothing changed.**
- The Payout Odds rule needs a default TradingView combo with PF >= 1.15 on >= 100 trades, above its fade, with an audit that is not invalid. For this pre-registered test it also needs a verdict that allows it (SPEC: Monte Carlo and Payout Odds only "if it holds up").
- Gold 15m X0 meets the numbers (1.204 on 440 trades, fade 0.771). But the verdict is DOES NOT HOLD UP, 15m is a lead and not the decision row, and local gold 15m is 0.857.
- leaders.json records this ("leaders": [], "meetNumericBarOnly": gold 15m).

### 12. Status of the to-do list
1. Open the browser and approve tradingview.com: **done** in the follow-up run.
2. Run P1 (and everything else) on Strategy Lab MPnDSp2M with unsaved scripts, recording B-ADJ: **done**. All 86 combos ran, and B-ADJ was ON and untouched.
3. Cross-check: **done**, both pass (NQ 72/72, GC 77/79).
4. Fill lab_rows.json, run make_results.py and the build: **done**. make_results.py now also computes checks (a)-(c), the TradingView pairs, the null, the reel window, the leads and the Payout gate, and asserts the verdict.
5. Rewrite the TradingView part of REEL14_NOTE: **done**.
6. Republish Strategy Lab Results (6xHJFsa82ZXJKh18jhDRPX): **left for the main session**. The files are ready; this step published nothing.

Still open (optional):
- Apply the audit's one-line fix (`not session.islastbar` in the cross gate) to the Pine Strats file.
- Fix the stale "status" text in local_results.json's xcheck block.
- Pre-register the V-1D NQ lead with local data first, if the user wants to pursue it.

The verdict cannot change.

_Updated 21 Oct 2026 after the TradingView run (make_results.py, patch_build_data_reel14tv.py, patch_takeaway_reel14tv.py)._
