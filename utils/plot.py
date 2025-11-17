# utils/plot.py
# 使用 Plotly 畫 K 線 + EMA + 買賣訊號

import plotly.graph_objects as go
import pandas as pd


def make_candlestick_with_signals(df: pd.DataFrame, symbol: str) -> go.Figure:
    fig = go.Figure()

    # =====================
    #   K 線
    # =====================
    fig.add_trace(
        go.Candlestick(
            x=df["time"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="K 線",
        )
    )

    # =====================
    #   EMA 快線 / 慢線
    # =====================
    fig.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["ema_fast"],
            mode="lines",
            name="EMA 快線",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["time"],
            y=df["ema_slow"],
            mode="lines",
            name="EMA 慢線",
        )
    )

    # =====================
    #   買入訊號 (三角形向上)
    # =====================
    buy_df = df[df["signal"] == "BUY"]
    fig.add_trace(
        go.Scatter(
            x=buy_df["time"],
            y=buy_df["signal_price"],
            mode="markers",
            name="買入訊號",
            marker=dict(symbol="triangle-up", size=12, color="green"),
        )
    )

    # =====================
    #   賣出訊號 (三角形向下)
    # =====================
    sell_df = df[df["signal"] == "SELL"]
    fig.add_trace(
        go.Scatter(
            x=sell_df["time"],
            y=sell_df["signal_price"],
            mode="markers",
            name="賣出訊號",
            marker=dict(symbol="triangle-down", size=12, color="red"),
        )
    )

    # =====================
    #   Layout
    # =====================
    fig.update_layout(
        title=f"{symbol} — 走勢圖與交易訊號",
        xaxis_title="時間",
        yaxis_title="價格",
        xaxis_rangeslider_visible=False,
        height=650,
    )

    return fig
