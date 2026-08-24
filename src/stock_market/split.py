from __future__ import annotations

import pandas as pd


def chronological_split(data: pd.DataFrame, train_end: str, validation_end: str,
                        purge_periods: int = 0):
    train_end_ts, validation_end_ts = pd.Timestamp(train_end), pd.Timestamp(validation_end)
    if train_end_ts >= validation_end_ts:
        raise ValueError("train_end must be before validation_end")
    ts = pd.to_datetime(data["timestamp"])
    dates = pd.Index(sorted(ts.unique()))
    train_dates = dates[dates <= train_end_ts]
    validation_dates = dates[(dates > train_end_ts) & (dates <= validation_end_ts)]
    if purge_periods:
        if len(train_dates) <= purge_periods or len(validation_dates) <= purge_periods:
            raise ValueError("Not enough dates for the requested purge period")
        train_dates = train_dates[:-purge_periods]
        validation_dates = validation_dates[:-purge_periods]
    train = data.loc[ts.isin(train_dates)].copy()
    validation = data.loc[ts.isin(validation_dates)].copy()
    test = data.loc[ts > validation_end_ts].copy()
    if any(part.empty for part in (train, validation, test)):
        raise ValueError("One split is empty; adjust dates to match the dataset")
    return train, validation, test
