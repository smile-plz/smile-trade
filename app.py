# app.py
# smile-trade — 歷史 K 線 + 即時 K 線 WebSocket

import streamlit as st
import pandas as pd
import time

from core.data_fetch import fetch_ohlcv
from core.signals import add_signals
from utils.plot import make_candlestick_with_signals
from core.realtime import LiveKline


# =====================================================
# 主程式
# =====================================================
def main():
    st.set_page_config(page_title="smile trade", layout="wide")

    st.title("📈 smile trade — 即時 / 歷史 K 線分析平台")
    st.caption("僅供學習與策略研究使用，不構成投資建議。")

    # --------------------
    # Sidebar 設定
    # --------------------
    st.sidebar.header("基本設定")

    symbol = st.sidebar.text_input("交易對（Binance）", value="BTC/USDT")
    timeframe = st.sidebar.selectbox(
        "時間週期",
        ["1m", "5m", "15m", "1h"],
        index=2,
    )

    mode = st.sidebar.radio(
        "資料模式",
        ["歷史 K 線（按一次抓取）", "即時 K 線（WebSocket 自動更新）"]
    )

    st.sidebar.header("策略參數（EMA + RSI）")
    fast = st.sidebar.number_input("EMA 快線週期", 3, 50, 9)
    slow = st.sidebar.number_input("EMA 慢線週期", 5, 200, 21)
    rsi_period = st.sidebar.number_input("RSI 週期", 5, 50, 14)
    rsi_buy = st.sidebar.slider("RSI 買入門檻", 40, 70, 55)
    rsi_sell = st.sidebar.slider("RSI 賣出門檻", 30, 60, 45)

    # =====================================================
    # 模式 1：歷史 K 線
    # =====================================================
    if mode == "歷史 K 線（按一次抓取）":
        st.subheader("📜 歷史 K 線模式")

        limit = st.sidebar.slider("下載 K 棒數量", 100, 1000, 300, 50)
        run = st.sidebar.button("開始分析")

        if not run:
            st.info("請按下『開始分析』")
            return

        with st.spinner("下載 K 線資料中…"):
            df = fetch_ohlcv(symbol, timeframe, limit)
            df = add_signals(df, fast, slow, rsi_period, rsi_buy, rsi_sell)

        fig = make_candlestick_with_signals(df, f"{symbol} @ {timeframe}")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📌 最近 50 根資料")
        st.dataframe(df.tail(50), use_container_width=True)

        return

    # =====================================================
    # 模式 2：即時 K 線 WebSocket
    # =====================================================
    st.subheader("⚡ 即時 K 線模式（WebSocket）")

    # Binance WebSocket 使用 btcusdt 這種格式
    symbol_ws = symbol.replace("/", "").lower()

    live = LiveKline(symbol=symbol_ws, interval=timeframe)
    live.start()

    st.success(f"已啟動 WebSocket：{symbol_ws} @ {timeframe}")

    placeholder = st.empty()

    # 每秒更新一次
    for _ in range(9999):
        # 取得最新 k 線資料
        with live.lock:
            df_live = live.df.copy()

        if len(df_live) > 10:
            # 計算策略指標
            df_live = add_signals(df_live, fast, slow, rsi_period, rsi_buy, rsi_sell)

            # 繪圖
            fig = make_candlestick_with_signals(df_live, f"{symbol}（即時）")
            placeholder.plotly_chart(fig, use_container_width=True)

        time.sleep(1)


if __name__ == "__main__":
    main()
