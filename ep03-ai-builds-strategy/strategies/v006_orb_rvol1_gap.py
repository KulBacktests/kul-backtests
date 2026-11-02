"""
v006 - v004 with the opening-volume filter relaxed to "above its trailing average".  Parent: v004_orb_rvol_gap
(via v005's delay+duration time encoding, which is non-behavioral; window back to 9:45-11:00).

Change vs parent (one thing): min_rvol 1.2 -> 1.0. Reason: the trade-count gate needs more qualifying
DAYS (v005 showed more hours does not help). "Opening-range volume above its 14-day average" is the
cleanest statement of the participation condition; 1.2x was an arbitrary margin on top of it.
"""
import numpy as np
import pandas as pd

PARAMS = dict(
    or_minutes=15,
    entry_delay_min=0,      # entries allowed from OR close + this
    entry_window_min=75,    # 9:45 -> 11:00
    target_R=2.0,
    min_range_pts=20.0,
    max_range_pts=150.0,
    min_rvol=1.0,
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

    rth = (df["minute_of_day"] >= open_min) & (df["minute_of_day"] < 16 * 60)
    rth_close = df["close"].where(rth).groupby(df["date"]).last()
    day_open = df["open"].where(df["minute_of_day"] == open_min).groupby(df["date"]).first()
    gap = df["date"].map(day_open - rth_close.shift(1))

    entry_start = open_min + p["or_minutes"] + p["entry_delay_min"]
    entry_end = entry_start + p["entry_window_min"]
    window = (df["minute_of_day"] >= entry_start) & (df["minute_of_day"] < entry_end)
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
