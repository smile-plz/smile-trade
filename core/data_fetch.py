# core/data_fetch.py
# 負責從 Binance 抓 OHLCV K 線資料

from typing import Literal
import ccxt
import pandas as pd

# 初始化交易所
_exchange = ccxt.binance({
    "enableRateLimit": True,
})


def fetch_ohlcv(
    symbol: str,
    timeframe: Literal["1m", "5m", "15m", "1h", "4h"] = "15m",
    limit: int = 300,
) -> pd.DataFrame:
    """
    從 Binance 取得 OHLCV 資料
    回傳 columns: [timestamp, open, high, low, close, volume, time]
    """
    ohlcv = _exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(
        ohlcv,
        columns=["timestamp", "open", "high", "low", "close", "volume"],
    )
    df["time"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df
