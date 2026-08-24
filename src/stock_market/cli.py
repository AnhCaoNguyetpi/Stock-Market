import argparse
from pathlib import Path
import yaml
from .data import load_all
from .features import add_features
from .labels import add_risk_label
from .model import RiskModel
from .split import chronological_split

RISK_FEATURES = ["open", "high", "low", "close", "volume", "ema_50", "ema_200",
 "macd", "macd_signal", "macd_diff", "rsi", "bollinger_hband", "bollinger_lband",
 "mfi", "return", "bollinger_pct", "bollinger_bw", "volatility_5d", "volatility_10d",
 "volume_change", "obv", "volume_pct_20d", "close_lag1", "close_lag2", "close_lag3",
 "return_lag1", "return_lag2", "return_lag3", "rsi_lag1", "rsi_lag2", "rsi_lag3"]


def main():
    parser = argparse.ArgumentParser(description="Leakage-safe Vietnam stock pipeline")
    parser.add_argument("--config", default="configs/default.yaml")
    sub = parser.add_subparsers(dest="command", required=True)
    command = sub.add_parser("train-risk")
    command.add_argument("--output", default="artifacts")
    args = parser.parse_args()
    with open(args.config, encoding="utf-8") as stream:
        config = yaml.safe_load(stream)
    paths = {"HOSE": config["data"]["hose"], "HNX": config["data"]["hnx"],
             "UPCOM": config["data"]["upcom"]}
    data = add_risk_label(add_features(load_all(paths)), **config["labels"])
    train, validation, test = chronological_split(data, **config["split"])
    for exchange in ("HOSE", "HNX", "UPCOM"):
        features = [feature for feature in RISK_FEATURES if feature in data.columns]
        model = RiskModel(features).fit(train[train.exchange == exchange])
        print(f"\n[{exchange}] validation\n{model.report(validation[validation.exchange == exchange])}")
        print(f"[{exchange}] final test\n{model.report(test[test.exchange == exchange])}")
        model.save(Path(args.output) / f"risk_{exchange.lower()}.joblib")


if __name__ == "__main__":
    main()

