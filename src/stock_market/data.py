from __future__ import annotations

from pathlib import Path
import pandas as pd

EXCHANGE_ALIASES = {"VN": "HOSE", "VNINDEX": "HOSE", "HSX": "HOSE", "HOSE": "HOSE",
                    "HNX": "HNX", "HNXINDEX": "HNX", "UPCOM": "UPCOM"}
REQUIRED_COLUMNS = {"timestamp", "ticker", "open", "high", "low", "close", "volume"}


def normalize_exchange(value: str) -> str:
    key = str(value).strip().upper()
    if key not in EXCHANGE_ALIASES:
        raise ValueError(f"Unknown exchange: {value!r}")
    return EXCHANGE_ALIASES[key]


def load_market_file(path: str | Path, exchange: str) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Missing input file: {path}")
    df = pd.read_excel(path)
    df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed:")].copy()
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"{path} is missing columns: {sorted(missing)}")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="raise")
    df["ticker"] = df["ticker"].astype(str).str.strip().str.upper()
    df["exchange"] = normalize_exchange(exchange)
    df = df.sort_values(["ticker", "timestamp"])
    duplicates = df.duplicated(["ticker", "timestamp"])
    if duplicates.any():
        raise ValueError(f"{path} has {int(duplicates.sum())} duplicate ticker-date rows")
    if (df[["open", "high", "low", "close", "volume"]].lt(0)).any().any():
        raise ValueError(f"{path} contains negative price/volume values")
    return df.reset_index(drop=True)


def load_all(paths: dict[str, str]) -> pd.DataFrame:
    frames = [load_market_file(path, exchange) for exchange, path in paths.items()]
    return pd.concat(frames, ignore_index=True).sort_values(["timestamp", "ticker"])

