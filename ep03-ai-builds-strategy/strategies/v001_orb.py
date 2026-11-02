"""
v001 — Opening Range Breakout, VWAP-side filter.

Hypothesis: the first N minutes after the 9:30 ET open establish a range; a close
outside that range, on the same side of session VWAP, carries momentum for the next
30-90 minutes. Only trades the morning; stops at range midpoint; target = R multiple.
One trade per side per day.

Every number below is a PARAM so the harness can sensitivity-test it.
"""
import numpy as np
import pandas as pd

PARAMS = dict(
    or_minutes=15,        # opening range length after 9:30
    entry_start=9 * 60 + 45,
    entry_end=11 * 60,    # no new entries after 11:00 ET
    target_R=2.0,         # reward:risk multiple
    min_range_pts=20.0,   # skip dead opens
    max_range_pts=150.0,  # skip crazy opens
)

def generate_signals(df, p):
    open_min = 9 * 60 + 30
    df["cum_pv"] = (df["close"] * df["volume"]).groupby(df["date"]).cumsum()
    df["cum_v"] = df["volume"].groupby(df["date"]).cumsum()
    df["vwap"] = np.where(df["cum_v"] > 0, df["cum_pv"] / df["cum_v"].replace(0, np.nan), df["close"])

    in_or = (df["minute_of_day"] >= open_min) & (df["minute_of_day"] < open_min + p["or_minutes"])
    or_hi = df["high"].where(in_or).groupby(df["date"]).transform("max")
    or_lo = df["low"].where(in_or).groupby(df["date"]).transform("min")
    rng = or_hi - or_lo
    mid = (or_hi + or_lo) / 2

    window = (df["minute_of_day"] >= p["entry_start"]) & (df["minute_of_day"] < p["entry_end"])
    ok_range = (rng >= p["min_range_pts"]) & (rng <= p["max_range_pts"])
    long_c = window & ok_range & (df["close"] > or_hi) & (df["close"] > df["vwap"])
    short_c = window & ok_range & (df["close"] < or_lo) & (df["close"] < df["vwap"])

    # first breakout per side per day only
    first_long = long_c & (~long_c.groupby(df["date"]).cumsum().shift(1, fill_value=0).astype(bool))
    first_short = short_c & (~short_c.groupby(df["date"]).cumsum().shift(1, fill_value=0).astype(bool))

    sig = pd.DataFrame(index=df.index)
    sig["signal"] = np.where(first_long, 1, np.where(first_short, -1, 0))
    risk_l = df["close"] - mid
    risk_s = mid - df["close"]
    sig["stop"] = np.where(first_long, mid, np.where(first_short, mid, np.nan))
    sig["target"] = np.where(first_long, df["close"] + p["target_R"] * risk_l,
                     np.where(first_short, df["close"] - p["target_R"] * risk_s, np.nan))
    return sig
