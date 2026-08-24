import numpy as np
import pandas as pd
import pytest
from stock_market.data import normalize_exchange
from stock_market.labels import add_risk_label, add_signal_label
from stock_market.split import chronological_split
from stock_market.backtest import backtest_next_open


def frame():
    dates = pd.date_range("2024-01-01", periods=8)
    return pd.DataFrame({"timestamp": list(dates) * 2, "ticker": ["AAA"] * 8 + ["BBB"] * 8,
        "close": [10] * 8 + [100] * 8,
        "low": [10, 9, 8, 7, 6, 5, 4, 3] + [100, 99, 98, 97, 96, 95, 94, 93]})


def test_exchange_names_are_canonical():
    assert normalize_exchange("VN") == normalize_exchange("hsx") == "HOSE"
    with pytest.raises(ValueError):
        normalize_exchange("UNKNOWN")


def test_future_window_never_crosses_tickers():
    result = add_risk_label(frame(), horizon=2)
    assert np.isnan(result[result.ticker == "AAA"].iloc[-1].future_min_low)
    assert result[result.ticker == "BBB"].iloc[0].future_min_low == 98


def test_signal_tail_is_unlabelled():
    result = add_signal_label(frame(), horizon=2)
    assert np.isnan(result[result.ticker == "AAA"].iloc[-1].signal_label)


def test_split_has_no_overlap():
    train, validation, test = chronological_split(frame(), "2024-01-03", "2024-01-05")
    assert train.timestamp.max() < validation.timestamp.min() < test.timestamp.min()


def test_backtest_uses_next_open_and_round_lot():
    dates = pd.date_range("2024-01-01", periods=2)
    data = pd.DataFrame({"timestamp": dates, "ticker": ["AAA", "AAA"],
                         "open": [10, 11], "close": [10, 12], "signal": [2, 1]})
    _, trades = backtest_next_open(data, initial_cash=100_000, max_positions=1,
                                    allocation=1.0)
    assert trades.iloc[0].timestamp == dates[1]
    assert trades.iloc[0].shares % 100 == 0
