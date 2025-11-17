# core/signals.py
# 技術指標組合成買賣訊號

import numpy as np
import pandas as pd

from core.indicators import ema, rsi


def add_signals(
    df: pd.DataFrame,
    fast: int = 9,
    slow: int = 21,
    rsi_period: int = 14,
    rsi_buy: float = 55.0,
    rsi_sell: float = 45.0,
) -> pd.DataFrame:
    """
    在 DataFrame 上加入：
      - ema_fast, ema_slow
      - rsi
      - signal: BUY / SELL / ""
      - signal_price
    """
    df = df.copy()

    # 計算指標
    df["ema_fast"] = ema(df["close"], fast)
    df["ema_slow"] = ema(df["close"], slow)
    df["rsi"] = rsi(df["close"], rsi_period)

    df["signal"] = ""
    df["signal_price"] = np.nan

    # BUY 條件：EMA 黃金交叉 + RSI 偏多
    buy_cond = (
        (df["ema_fast"] > df["ema_slow"]) &
        (df["ema_fast"].shift(1) <= df["ema_slow"].shift(1)) &
        (df["rsi"] > rsi_buy)
    )

    # SELL 條件：EMA 死亡交叉 + RSI 偏空
    sell_cond = (
        (df["ema_fast"] < df["ema_slow"]) &
        (df["ema_fast"].shift(1) >= df["ema_slow"].shift(1)) &
        (df["rsi"] < rsi_sell)
    )

    df.loc[buy_cond, "signal"] = "BUY"
    df.loc[sell_cond, "signal"] = "SELL"
    df.loc[df["signal"] != "", "signal_price"] = df["close"]

    return df
