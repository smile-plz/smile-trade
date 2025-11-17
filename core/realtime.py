# core/realtime.py
# Binance WebSocket 即時 K 線處理

import threading
from binance import ThreadedWebsocketManager
import pandas as pd


class LiveKline:
    def __init__(self, symbol="btcusdt", interval="15m"):
        self.symbol = symbol.lower()
        self.interval = interval
        self.df = pd.DataFrame()
        self.lock = threading.Lock()
        self.twm = None

    def _socket_handler(self, msg):
        # 必須是 K 線事件
        if msg.get("e") != "kline":
            return

        k = msg["k"]

        new_row = {
            "time": pd.to_datetime(k["t"], unit="ms"),
            "open": float(k["o"]),
            "high": float(k["h"]),
            "low": float(k["l"]),
            "close": float(k["c"]),
            "volume": float(k["v"]),
        }

        # 更新 K 線資料（含防重複）
        with self.lock:
            self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
            self.df = self.df.drop_duplicates(subset=["time"], keep="last")

    def start(self):
        # 啟動 WebSocket
        self.twm = ThreadedWebsocketManager()
        self.twm.start()
        self.twm.start_kline_socket(
            callback=self._socket_handler,
            symbol=self.symbol,
            interval=self.interval,
        )

    def stop(self):
        if self.twm:
            self.twm.stop()
