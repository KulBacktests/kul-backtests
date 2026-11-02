"""
v004 — v003 + overnight-gap direction agreement.  Parent: v003_orb_rvol.

Change vs parent (one thing): only take longs when today's 9:30 open is above the prior RTH
close (gap up) and shorts when it is below (gap down). Reason: a gap leaves the prior session's
positioning offside; a breakout in the gap direction squeezes those traders, a breakout against
it is a gap-fill and tends to stall at the prior close. Everything else identical to v003.
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

    or_vol = df["volume"].where(in_or).groupby(df["date"]).sum()
    ref = or_vol.shift(1).rolling(int(p["rvol_days"]), min_periods=5).mean()
    rvol = df["date"].map(or_vol / ref)

    # overnight gap: today's 9:30 open vs prior RTH close (last bar before 16:00 ET, prior date). shift(1): no lookahead.
    rth = (df["minute_of_day"] >= open_min) & (df["minute_of_day"] < 16 * 60)
    rth_close = df["close"].where(rth).groupby(df["date"]).last()
    day_open = df["open"].where(df["minute_of_day"] == open_min).groupby(df["date"]).first()
    gap = df["date"].map(day_open - rth_close.shift(1))

    window = (df["minute_of_day"] >= p["entry_start"]) & (df["minute_of_day"] < p["entry_end"])
    ok_range = (rng >= p["min_range_pts"]) & (rng <= p["max_range_pts"]) & (rvol >= p["min_rvol"])
    long_c = window & ok_range & (gap > 0) & (df["close"] > or_hi) & (df["close"] > df["vwap"])
    short_c = window & ok_range & (gap < 0) & (df["close"] < or_lo) & (df["close"] < df["vwap"])

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
