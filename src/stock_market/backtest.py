from __future__ import annotations

from dataclasses import dataclass
import pandas as pd


@dataclass(frozen=True)
class Costs:
    commission: float = 0.0015
    sell_tax: float = 0.001
    slippage: float = 0.001


def backtest_next_open(data: pd.DataFrame, initial_cash: float = 1_000_000_000,
                       max_positions: int = 15, allocation: float = 1 / 15,
                       costs: Costs = Costs()) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Execute prior-close signals at next open; signal: 2 buy, 0 sell, 1 hold."""
    required = {"timestamp", "ticker", "open", "close", "signal"}
    if missing := required - set(data.columns):
        raise ValueError(f"Missing backtest columns: {sorted(missing)}")
    df = data.sort_values(["timestamp", "ticker"]).copy()
    df["order"] = df.groupby("ticker")["signal"].shift(1)
    cash, holdings, trades, equity = float(initial_cash), {}, [], []
    for date, day in df.groupby("timestamp", sort=True):
        rows = day.set_index("ticker")
        for ticker in list(holdings):
            if ticker in rows.index and rows.at[ticker, "order"] == 0:
                shares = holdings.pop(ticker)
                price = rows.at[ticker, "open"] * (1 - costs.slippage)
                proceeds = shares * price * (1 - costs.commission - costs.sell_tax)
                cash += proceeds
                trades.append({"timestamp": date, "ticker": ticker, "side": "SELL",
                               "shares": shares, "price": price})
        slots = max_positions - len(holdings)
        candidates = rows[(rows.order == 2) & ~rows.index.isin(holdings)].head(slots)
        for ticker, row in candidates.iterrows():
            budget = min(initial_cash * allocation, cash)
            price = row.open * (1 + costs.slippage)
            shares = int(budget / (price * (1 + costs.commission)) / 100) * 100
            if shares > 0:
                cash -= shares * price * (1 + costs.commission)
                holdings[ticker] = shares
                trades.append({"timestamp": date, "ticker": ticker, "side": "BUY",
                               "shares": shares, "price": price})
        market_value = sum(shares * rows.at[ticker, "close"] for ticker, shares in holdings.items()
                           if ticker in rows.index)
        equity.append({"timestamp": date, "cash": cash, "market_value": market_value,
                       "equity": cash + market_value, "positions": len(holdings)})
    return pd.DataFrame(equity), pd.DataFrame(trades)
