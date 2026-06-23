from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from app.ml.forecasting import ForecastMetrics, TrafficForecastEngine


class ModelScorecard:
    def __init__(self):
        self.results: Dict[str, ForecastMetrics] = {}

    def add(self, model_name: str, metrics: ForecastMetrics):
        self.results[model_name] = metrics

    def best_model(self) -> Optional[str]:
        if not self.results:
            return None
        return min(self.results, key=lambda k: self.results[k].rmse)

    def to_dict(self) -> Dict[str, Dict[str, float]]:
        return {name: metric.__dict__ for name, metric in self.results.items()}


class ForecastPipeline:
    def __init__(self, model_dir: str = "./backend/app/ml/models"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.engine = TrafficForecastEngine()

    def load_dataset(self, csv_path: str) -> pd.DataFrame:
        df = pd.read_csv(csv_path, parse_dates=["timestamp"])
        if "timestamp" not in df.columns:
            raise ValueError("Dataset requires a 'timestamp' column.")
        return df.sort_values("timestamp").reset_index(drop=True)

    def prepare_features(self, df: pd.DataFrame, target_column: str) -> pd.DataFrame:
        return self.engine._build_lag_features(df, target_column)

    def train_models(self, df: pd.DataFrame, target_column: str) -> ModelScorecard:
        features = [col for col in df.columns if col != target_column and col != "timestamp"]
        X = df[features]
        y = df[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        scorecard = ModelScorecard()
        for name, model in self.engine.models.items():
            fitted = model.fit(X_train, y_train)
            y_pred = fitted.predict(X_test)
            metrics = self.engine._evaluate(y_test.values, y_pred)
            scorecard.add(name, metrics)
        return scorecard

    def train_from_csv(self, csv_path: str, target_column: str = "concurrent_users") -> Dict[str, object]:
        df = self.load_dataset(csv_path)
        prepared = self.prepare_features(df, target_column)
        scorecard = self.train_models(prepared, target_column)
        return {
            "best_model": scorecard.best_model(),
            "metrics": scorecard.to_dict(),
        }
