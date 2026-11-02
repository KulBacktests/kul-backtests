"""
v002 — ORB with range filter normalized by recent RTH daily range.  Parent: v001_orb.

Change vs parent (one thing): the opening-range size filter is expressed as a fraction of the
trailing 14-day mean RTH range instead of fixed points. Reason: NQ went 15k -> 20k inside the
train window, so "20 to 150 points" meant different volatility regimes at each end of the sample.
Thresholds chosen to match v001's semantics at the sample midpoint (~200-pt daily RTH range):
20/200 = 0.10, 150/200 = 0.75.  Everything else identical to v001.
"""
import numpy as np
import pandas as pd

PARAMS = dict(
    or_minutes=15,
    entry_start=9 * 60 + 45,
    entry_end=11 * 60,
    target_R=2.0,
    min_range_frac=0.10,   # OR range / trailing mean RTH daily range
    max_range_frac=0.75,
    atr_days=14,
)

def daily_rth_range_ref(df, n):
    """Trailing mean of prior n days' RTH (9:30-16:00 ET) high-low range, aligned to each bar. No lookahead:
    today's range is excluded via shift(1) on the per-date series."""
    rth = (df["minute_of_day"] >= 9 * 60 + 30) & (df["minute_of_day"] < 16 * 60)
    d = df[rth].groupby("date").agg(hi=("high", "max"), lo=("low", "min"))
    rng = (d["hi"] - d["lo"]).shift(1).rolling(n, min_periods=max(3, n // 2)).mean()
    return df["date"].map(rng)

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
    ref = daily_rth_range_ref(df, int(p["atr_days"]))
    frac = rng / ref

    window = (df["minute_of_day"] >= p["entry_start"]) & (df["minute_of_day"] < p["entry_end"])
    ok_range = (frac >= p["min_range_frac"]) & (frac <= p["max_range_frac"])
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
