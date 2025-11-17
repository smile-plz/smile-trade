# core/indicators.py
# 各種技術指標：EMA、RSI

import numpy as np
import pandas as pd


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """
    RSI 的標準實作（不使用 talib）
    """
    delta = series.diff()

    gain = np.where(delta > 0, delta, 0.0)
    loss = np.where(delta < 0, -delta, 0.0)

    gain = pd.Series(gain, index=series.index).rolling(window=period).mean()
    loss = pd.Series(loss, index=series.index).rolling(window=period).mean()

    rs = gain / loss
    rsi_val = 100 - (100 / (1 + rs))
    return rsi_val
