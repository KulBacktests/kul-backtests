# Research journal

## v001_orb — baseline
Hypothesis: 15-min opening range breakout in the VWAP direction carries momentum through the morning.
Parent: none. Status: untested on real data.

### Data check (2026-09-18)
Continuous front-month NQ 1-min built from Databento per-contract CSV using btlab's roll schedule
(volume crossover from prior-day volume, never rolls back). 1,767,487 bars, 2021-01-31 -> 2026-01-28,
21 contracts, no gap > 3 calendar days. Timestamps UTC -> run with `NQ_TZ=UTC`. Unadjusted at rolls
(strategy is flat overnight so roll gaps never sit inside a trade). Note: btlab froze a holdout from
2025-06-01; the harness OOS window (2024-09-01 ->) overlaps it. OOS here is validation-only per CLAUDE.md.

### Round 0 — v001_orb baseline (IS 2021-09..2024-08)
trades=889 (0.95/day) | net=-12,170 | PF 0.98 | win 35.7% | maxDD -37,495 | stop 62% target 29% time 9%
- Every year negative; 2023 worst (-8.5k). Shorts PF 1.16, longs 0.81 despite an up-trending sample.
- 10:xx entries PF 0.89 vs 9:xx 1.04. Time-exits (76) are 75% winners: trades that don't resolve fast still drift right.
- avg win/avg loss = 1.76, not 2.0: slippage+commission on a ~40-pt risk eats ~10% of R.
- Fixed 20-150 pt range filter is non-stationary: NQ went 15k -> 20k in-sample, 20 pts is 0.13% in 2021 and 0.10% in 2024.
Learned: no edge as specified. First fix is the obvious stationarity bug, not a new indicator.

### Round 1 — v002_orb_atrnorm (parent v001)
Hypothesis: the fixed 20-150 pt range filter is non-stationary; expressing it as a fraction of trailing 14-day RTH range should stop it admitting the wrong days at each end of the sample.
Result: trades=907 | net=-25,462 | PF 0.95 | win 35.2% | maxDD -55,670 | stop 63%. Worse than v001.
- Trade set barely changed (907 vs 889): the filter was hardly binding either way. The losing months are the same (2022-01, 2022-07/08, 2023-07, 2024-06).
- Longs still PF 0.85 vs shorts 1.07. Time-exits still ~74% winners.
Learned: range size is not the discriminating variable. Abandon this branch (fix was correct in principle, but there was nothing behind it to fix). Back to v001 as parent.

### Round 2 — v003_orb_rvol (parent v001)
Hypothesis: breakouts need participation; require opening-range volume >= 1.2x its trailing 14-day mean.
Result: trades=444 (0.48/day) | net=+33,260 | PF 1.13 | win 39.6% | maxDD -16,028 | Sharpe 0.58 | stop 57%.
- First version positive in every year (2021 1.12, 2022 1.18, 2023 1.00, 2024 1.23). Halved the trade count, tripled per-trade avg.
- Still gated out: PF 1.13 < 1.25. 2023 is flat: the losing months are Jun-Aug 2023 (low-vol grind).
- Persistent asymmetry: shorts PF 1.47 / longs 0.83 in all three versions so far. Not acting on it yet: a long/short switch is exactly the kind of parameter that looks structural and is sample noise. Will revisit only if it survives OOS untouched.
- Time-exits again 75% winners, PF 8: trades that run to the close without resolving are trend days. The 2R cap may be leaving money; parked as a "how" change for later.
- 2022-10 alone is +14.6k of the +33k (top 5% of trades = 23% of gross profit, acceptable).
Learned: participation is the discriminating variable, not range size. Iterate on this branch.

### Round 3 — v004_orb_rvol_gap (parent v003)
Hypothesis: only trade the breakout in the direction of the overnight gap (open vs prior RTH close); a gap leaves the prior session offside and the breakout squeezes it, a counter-gap breakout is a gap-fill that stalls at the prior close.
Result: trades=180 (0.19/day) | net=+41,478 | PF 1.47 | win 44.4% | maxDD -7,692 | Sharpe 1.17 | stop 51%.
- FAILS only on trade count (<200). Every year positive (2.40 / 1.48 / 1.37 / 1.24, declining). Both sides positive for the first time (longs 1.26, shorts 1.66): the long/short asymmetry was mostly counter-gap longs.
- Top 5% of trades = 20% of gross profit. 9:xx entries PF 1.55, 10:xx 1.35, no reason to cut the window.
- 2024 is the weakest year (1.24 on 43 trades): the edge may be fading or 2024 was just quieter.
- Filter cut 444 -> 180 trades. That is more than "half the days gap the wrong way" would explain, so the gap filter is interacting with rvol (high-rvol days with a gap in the breakout direction). Fine structurally, but small n.
Learned: gap + participation is the combination. Round 4 = scheduled OOS + sensitivity on v004 before touching anything else, because the next in-sample move must widen the trade set and I want to know whether the edge is real first.

### Round 4 — scheduled OOS + sensitivity + Monte Carlo on v004 (no new version)
OOS 2024-09-01 -> 2026-01-28 (data end): trades=60 | net=+24,368 | PF 1.67 | win 48.3% | maxDD -6,478 | Sharpe 1.35. Nothing was tuned before or after looking.
Sensitivity (IS):
- FLAGGED entry_start x0.8/x0.9/x1.2 and entry_end x0.8: artifacts. The harness scales clock minutes, so 9:45 -> 7:48 / 8:46 (entering before the opening range exists) or start > end (zero trades). Not real fragility; the time window must be encoded as offset + duration so the test means something. Fixing that in v005.
- Genuine wobble, not flagged: or_minutes 12 -> PF 1.17, 16 -> 1.18 while 14 and 18 are 1.36/1.33. Non-monotonic = noise at n=180. min_rvol 0.96 -> 1.18, 1.08 -> 1.39, 1.32 -> 1.27, 1.44 -> 1.73: the 1.2 default sits in a bumpy region.
- min_range_pts is dead (16-24 identical results): rvol already excludes those days. Candidate for removal later.
- target_R 1.6-2.4 all PF 1.36-1.51: robust. max_range_pts, rvol_days: 1.25-1.39, fine.
Monte Carlo (IS, 180 trades): median maxDD -9,754 | 95th pct -15,320 | worst -22,672 | P(net<0) 1.4%.
Decision: edge looks real but 180+60 trades is thin. Next: widen the trade set (extend entry window to noon), not tighten anything.

### Round 5 — v005_orb_rvol_gap_noon (parent v004)
Hypothesis: on gap + participation days the first breakout can come late morning and still has time to run; extend entries to 12:00.
Result: trades=194 | net=+34,828 | PF 1.35 | Sharpe 0.96 | stop 53%. Worse than v004.
- Only 14 trades added (11:00-12:00), 13 in-sample, and they were -5,752 at PF 0.39 / 23% win. The first breakout on a qualifying day happens before 11:00 on ~93% of days; the ones that break late are the weak ones.
- Also re-encoded the time window as delay + duration (non-behavioral) so sensitivity is meaningful. Keep that encoding.
Learned: entry window is right at 9:45-11:00; late breakouts are a fade, not a continuation. Abandon. Trade count has to come from admitting more *days*, not more *hours*. Parent for v006 = v004 (with the v005 time encoding).

### Round 6 — v006_orb_rvol1_gap (parent v004)
Hypothesis: "opening volume above its trailing average" (1.0x) is the natural participation condition; the 1.2x margin was arbitrary and starves the sample.
Result: trades=307 (0.33/day) | net=+40,915 | PF 1.26 | win 41% | maxDD -13,460 | Sharpe 0.93 | stop 56%. PASSES gates (PF 1.26 vs 1.25 is a hair).
- The 127 added trades (rvol 1.0-1.2) net roughly zero: net barely moved (41.5k -> 40.9k) while maxDD nearly doubled. Dilution, not edge.
- By year: 1.87 / 1.40 / 1.11 / 1.00. Monotonic decay. 2024 is flat on 66 trades. Either the edge is fading or the 2024 low-vol grind is hostile to it; v004 showed the same shape at 2.40/1.48/1.37/1.24.
- 10:xx entries PF 1.07 vs 9:xx 1.40; in v004 they were 1.35 vs 1.55. The marginal rvol days are the ones that break out late.
Learned: rvol 1.2 -> 1.0 buys sample size at the cost of quality; gate pass is marginal. Running OOS + sensitivity on it as the rules require, but v004 is the cleaner statement of the idea.

### Round 7 — validation of v006 (no new version). STOP RULE TRIGGERED.
OOS 2024-09-01 -> 2026-01-28: trades=108 | net=+32,650 | PF 1.51 | win 45.4% | maxDD -8,350 | Sharpe 1.46.
Sensitivity (IS): no fragile flags. Every param in PF 1.15-1.47 across +/-20%. min_range_pts is dead weight (identical at all values).
Monte Carlo (IS, 307 trades): median maxDD -14,105 | 95th pct -22,047 | worst -35,110 | P(net<0) 3.3%.
Lookahead check: shifting every entry one bar later gives IS PF 1.25 / OOS PF 1.63. A lookahead edge collapses under this; this one does not move.
Honest reading of OOS: 2024 Q4 PF 2.62 (25 trades), full-year 2025 PF 1.17 (78 trades, just above the 1.15 gate), Jan 2026 5 trades. The OOS aggregate is flattered by Q4 2024. Longs carried OOS (1.69) where shorts carried IS (1.39): the side asymmetry flips between samples, which is the right reason never to have conditioned on it.
Caveat: the OOS window overlaps btlab's frozen NQ holdout (from 2025-06-01). This loop's OOS is validation-only and was looked at twice (rounds 4 and 7), never tuned to.
v006 passes gates + sensitivity + OOS -> CLAUDE.md says stop and report. Stopping at round 7 of 12.

## Session summary (2026-09-18)
**Best candidate: v006_orb_rvol1_gap.** Two-sentence version: on days where the first 15 minutes trade above their 14-day average volume, take the first 1-min close outside the opening range between 9:45 and 11:00, but only in the direction of the overnight gap (open vs prior RTH close) and on the VWAP side. Stop at the range midpoint, target 2R, flat by 15:58.
- IS 2021-09..2024-08: 307 trades, PF 1.26, Sharpe 0.93, maxDD -13.5k, net +40.9k (1 NQ, $5 RT, 1.5 ticks/side slippage, stop-first fills).
- OOS 2024-09..2026-01: 108 trades, PF 1.51, Sharpe 1.46, maxDD -8.4k, net +32.7k. Full-year 2025 alone PF 1.17.
- Sensitivity: nothing fragile. Monte Carlo 95th-pct DD -22k on 3 years of IS trades.
- Weaknesses: IS PF 1.26 is a hair over the gate; IS by-year decays 1.87 -> 1.40 -> 1.11 -> 1.00 before recovering OOS; 0.3 trades/day is slow. v004 (rvol 1.2) is the same idea with better per-trade stats (IS PF 1.47, OOS 1.67) but only 180 IS trades.
**Dead branches:** (1) normalizing the range filter by trailing daily range (v002): range size is not the variable, filter was never binding. (2) Extending entries past 11:00 (v005): late breakouts on qualifying days lose (PF 0.39); the first breakout comes before 11:00 on 93% of days anyway.
**Not tried on purpose:** long/short conditioning (asymmetry flipped between IS and OOS), removing dead min_range_pts (cosmetic, would be a version with no behavioral change), lowering rvol below 1.0 (sensitivity shows a cliff at 0.8-0.9).
**Three ideas next:**
1. Trade management on trend days: time-exits are 70-76% winners with PF 7-9 in every version. Test a trailing stop (e.g. move stop to breakeven at 1R) or target 3R with a 1R breakeven stop. It is a "how" change, so do it only on v006 and accept it only if it survives sensitivity.
2. Gap size as a fraction of trailing daily range: direction alone is used now; a gap below ~10% of the daily range is noise and probably adds the marginal losing trades. One param, structurally motivated (small gaps do not trap anyone).
3. Extend the in-sample backwards: data exists from 2021-02 and TRAIN starts 2021-09. Adding 7 months lifts n without touching OOS; needs the user's OK since it changes the split in backtest.py.

### Round 8 — v007_orb_rvol1_gap_fixdays (parent v006): bug fix found while porting to Pine
Found: v006 (and v003-v005) built the per-date series over every ET calendar date. Sunday-evening and holiday dates have overnight bars but no RTH close, so Monday's gap was NaN and v006 never traded Mondays or the day after a holiday (IS weekday counts: Mon 0, Tue 85, Wed 76, Thu 68, Fri 78). Those dates also pushed zero opening-range volume into the 14-day mean, so the effective rvol threshold was ~0.8x of the true session mean, not 1.0x.
Fix: daily series restricted to dates with an RTH session. Signal logic unchanged.
Result IS: trades=223 | net=+34,822 | PF 1.29 | Sharpe 0.86 | maxDD -10,720. OOS: trades=72 | net=+21,768 | PF 1.46 | Sharpe 1.11 | maxDD -8,390. PASSES gates, no fragile params.
- Fewer trades than v006 (223 vs 307) because the volume reference is now honest; the added Mondays (40 trades, PF 0.92) roughly wash.
- Longs fell to PF 0.97 (shorts 1.65). By year 1.83 / 1.44 / 1.11 / 0.98, same decay shape as before.
- Sensitivity bumps: or_minutes 16 -> PF 1.11, min_rvol 1.1 -> 1.16. Not flagged, but the surface is not smooth at n=223.
Pine port: pine/nq_orb_gap_rvol_v007.pine (v6 strategy, all built-ins checked against the pine-script-v6 skill lookup; NOT compiled in TradingView, the MCP compile loop is not available here). Has a toggle to replicate v006's no-Monday quirk. Fill model in TV is more generous than the harness (stop-first assumption not replicable).
