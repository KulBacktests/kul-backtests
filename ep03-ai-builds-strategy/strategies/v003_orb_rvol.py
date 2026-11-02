"""
v003 — ORB with relative-volume filter on the opening range.  Parent: v001_orb.

Change vs parent (one thing): only trade days whose opening-range volume is at least `min_rvol`
times the trailing `rvol_days` mean of opening-range volume. Reason: a breakout needs
participation to carry; high relative volume in the first 15 minutes means institutions are
repositioning (the Zarattini/Carrion ORB result rests on this filter). Low-volume opens are
range-bound and their breakouts fade. Everything else identical to v001.
"""
import numpy as np
import pandas as pd

PARAMS = dict(
    or_minutes=15,
    entry_start=9 * 60 + 45,
    entry_end=11 * 60,
    target_R=2.0,
    min_range_pts=20.0,
    max_range_pts=150.0,
    min_rvol=1.2,
    rvol_days=14,
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

    # relative volume of the opening range vs prior days (shift(1) on the per-date series: no lookahead)
    or_vol = df["volume"].where(in_or).groupby(df["date"]).sum()
    ref = or_vol.shift(1).rolling(int(p["rvol_days"]), min_periods=5).mean()
    rvol = df["date"].map(or_vol / ref)

    window = (df["minute_of_day"] >= p["entry_start"]) & (df["minute_of_day"] < p["entry_end"])
    ok_range = (rng >= p["min_range_pts"]) & (rng <= p["max_range_pts"]) & (rvol >= p["min_rvol"])
    long_c = window & ok_range & (df["close"] > or_hi) & (df["close"] > df["vwap"])
    short_c = window & ok_range & (df["close"] < or_lo) & (df["close"] < df["vwap"])

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
