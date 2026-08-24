from __future__ import annotations

import numpy as np
import pandas as pd


def _future_min(series: pd.Series, horizon: int) -> pd.Series:
    # Reverse rolling computes min(t+1 ... t+horizon), never crossing a ticker.
    return series.shift(-1).iloc[::-1].rolling(horizon, min_periods=horizon).min().iloc[::-1]


def add_risk_label(data: pd.DataFrame, horizon: int = 10, quantile: float = 0.35) -> pd.DataFrame:
    if not 0 < quantile < 1 or horizon < 1:
        raise ValueError("quantile must be in (0, 1) and horizon must be positive")
    df = data.sort_values(["ticker", "timestamp"]).copy()
    df["future_min_low"] = df.groupby("ticker", group_keys=False)["low"].apply(
        lambda s: _future_min(s, horizon)
    )
    df["future_max_drawdown"] = df["future_min_low"] / df["close"] - 1
    # Cross-sectional threshold uses outcomes for that date only; labels are training targets, not features.
    threshold = df.groupby("timestamp")["future_max_drawdown"].transform(
        lambda s: s.quantile(quantile)
    )
    df["risk_label"] = np.where(df["future_max_drawdown"].isna(), np.nan,
                                (df["future_max_drawdown"] <= threshold).astype(float))
    return df


def add_signal_label(data: pd.DataFrame, horizon: int = 10, threshold: float = 0.02) -> pd.DataFrame:
    df = data.sort_values(["ticker", "timestamp"]).copy()
    future_close = df.groupby("ticker")["close"].shift(-horizon)
    df["future_return"] = future_close / df["close"] - 1
    df["signal_label"] = np.select(
        [df["future_return"] < -threshold, df["future_return"] > threshold], [0, 2], default=1
    ).astype(float)
    df.loc[df["future_return"].isna(), "signal_label"] = np.nan
    return df

