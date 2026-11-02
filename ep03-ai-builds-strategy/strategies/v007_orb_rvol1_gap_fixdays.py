"""
v007 - v006 with the daily reference series restricted to dates that have an RTH session.
Parent: v006_orb_rvol1_gap.

Change vs parent (one thing, a bug fix): in v006 the per-date series (opening-range volume, prior RTH
close) were built over every ET calendar date, including Sunday evenings and holidays that have
overnight bars but no 9:30-16:00 session. Consequences: (1) Monday's gap was open - NaN, so v006
never traded Mondays or the day after a holiday; (2) those dates contributed zero opening-range
volume to the 14-day mean, lowering the effective rvol threshold. v007 builds the daily series
only from dates with an RTH session, so the gap is measured against the last real RTH close and
the volume reference averages the last 14 real sessions. Signal logic is otherwise identical.
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

    # daily series over RTH sessions only (dates with no 9:30-16:00 bars are dropped, not zero-filled)
    rth = (df["minute_of_day"] >= open_min) & (df["minute_of_day"] < 16 * 60)
    daily = pd.DataFrame({
        "or_vol": df["volume"].where(in_or).groupby(df["date"]).sum(min_count=1),
        "rth_close": df["close"].where(rth).groupby(df["date"]).last(),
        "day_open": df["open"].where(df["minute_of_day"] == open_min).groupby(df["date"]).first(),
    })
    daily = daily[daily["rth_close"].notna()]
    daily["ref"] = daily["or_vol"].shift(1).rolling(int(p["rvol_days"]), min_periods=5).mean()
    daily["gap"] = daily["day_open"] - daily["rth_close"].shift(1)
    rvol = df["date"].map(daily["or_vol"] / daily["ref"])
    gap = df["date"].map(daily["gap"])

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
