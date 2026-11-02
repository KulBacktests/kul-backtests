# Paste this into Claude Code after opening the nq-loop folder

Read CLAUDE.md. My NQ 1-minute data is at data/nq_1min.csv (columns: timestamp,open,high,low,close,volume; timestamps in UTC, so run with NQ_TZ=UTC. Continuous front-month built from Databento per-contract data via btlab roll schedule (volume crossover, prior-day volume)).

1. Run `python backtest.py strategies/v001_orb.py --no-log` and confirm the data loaded cleanly:
   bar count, date range, days, any gaps > 3 trading days. Fix the loader if my columns differ.
2. Then start the loop from CLAUDE.md. Run up to 12 rounds. Change one thing per round,
   journal every round, run --oos only every 4th round, --sensitivity on any version that passes gates.
3. Stop early and report if anything in the "Stop and report" section triggers.
4. Finish with a summary: best candidate (with its IS/OOS/sensitivity/Monte Carlo numbers),
   the branches you abandoned and why, and the three ideas you'd try next.
