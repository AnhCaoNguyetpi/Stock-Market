from __future__ import annotations

import numpy as np
import pandas as pd


def add_features(data: pd.DataFrame) -> pd.DataFrame:
    """Create causal features. Every row uses only information available by that close."""
    df = data.sort_values(["ticker", "timestamp"]).copy()
    g = df.groupby("ticker", group_keys=False)
    if "return" not in df:
        df["return"] = g["close"].pct_change()
    df["volatility_5d"] = g["return"].rolling(5).std().reset_index(level=0, drop=True)
    df["volatility_10d"] = g["return"].rolling(10).std().reset_index(level=0, drop=True)
    df["volatility_20d"] = g["return"].rolling(20).std().reset_index(level=0, drop=True)
    df["volume_change"] = g["volume"].pct_change()
    df["obv"] = (np.sign(df["return"].fillna(0)) * df["volume"]).groupby(df["ticker"]).cumsum()
    df["volume_pct_20d"] = g["volume"].transform(
        lambda s: s.rolling(20).rank(pct=True)
    )
    for column in ("close", "return", "rsi", "macd", "macd_diff", "bollinger_pct"):
        if column in df:
            for lag in (1, 2, 3):
                df[f"{column}_lag{lag}"] = g[column].shift(lag)
    for lag in (5, 10, 15):
        df[f"return_lag_{lag}"] = g["return"].shift(lag)
    if "rsi" in df:
        df["rsi_momentum"] = g["rsi"].diff()
    if "macd_diff" in df:
        df["macd_diff_momentum"] = g["macd_diff"].diff()
    if "ema_200" in df:
        df["price_vs_ema200"] = df["close"] / df["ema_200"] - 1
    return df.replace([np.inf, -np.inf], np.nan)

