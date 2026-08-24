from pathlib import Path
import joblib
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.metrics import classification_report


class RiskModel:
    def __init__(self, features: list[str], threshold: float = 0.5, **params):
        self.features, self.threshold = features, threshold
        self.estimator = LGBMClassifier(objective="binary", random_state=42,
            n_estimators=400, learning_rate=0.03, class_weight="balanced", **params)

    def fit(self, data: pd.DataFrame):
        clean = data.dropna(subset=self.features + ["risk_label"])
        self.estimator.fit(clean[self.features], clean["risk_label"].astype(int))
        return self

    def predict(self, data: pd.DataFrame):
        return (self.estimator.predict_proba(data[self.features])[:, 1] >= self.threshold).astype(int)

    def report(self, data: pd.DataFrame) -> str:
        clean = data.dropna(subset=self.features + ["risk_label"])
        return classification_report(clean["risk_label"].astype(int), self.predict(clean), digits=4)

    def save(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({"features": self.features, "threshold": self.threshold,
                     "estimator": self.estimator}, path)

