from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


@dataclass
class ForecastMetrics:
    mae: float
    rmse: float
    mape: float
    r2: float


class TrafficForecastEngine:
    def __init__(self):
        self.horizons = [5, 15, 30, 60]
        self.models = {
            "random_forest": RandomForestRegressor(n_estimators=50, random_state=42),
        }

    @staticmethod
    def _build_lag_features(data: pd.DataFrame, target_column: str, lags: int = 3) -> pd.DataFrame:
        df = data.copy()
        for lag in range(1, lags + 1):
            df[f"lag_{lag}"] = df[target_column].shift(lag)
        return df.dropna()

    @staticmethod
    def _evaluate(y_true: np.ndarray, y_pred: np.ndarray) -> ForecastMetrics:
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mape = np.mean(np.abs((y_true - y_pred) / np.maximum(np.abs(y_true), 1))) * 100
        r2 = r2_score(y_true, y_pred) if len(y_true) > 1 else 0.0
        return ForecastMetrics(mae=mae, rmse=rmse, mape=mape, r2=r2)

    def compare_models(self, data: pd.DataFrame, target_column: str) -> Dict[str, ForecastMetrics]:
        df = self._build_lag_features(data, target_column)
        if df.empty:
            return {}

        features = [col for col in df.columns if col != target_column and col != "timestamp"]
        X = df[features]
        y = df[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        results: Dict[str, ForecastMetrics] = {}
        for name, model in self.models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            results[name] = self._evaluate(y_test.values, y_pred)

        return results

    def select_best_model(self, results: Dict[str, ForecastMetrics]) -> Optional[str]:
        if not results:
            return None
        return min(results, key=lambda k: results[k].rmse)

    def predict(self, input_data: Dict[str, float]) -> List[Dict[str, float]]:
        base_load = input_data.get("concurrent_users", 0)
        load_factor = input_data.get("requests_per_second", 0) * 0.02
        traffic_volume = input_data.get("traffic_volume_mb", 0)
        utilization = input_data.get("network_utilization", 0)

        predictions = []
        for horizon in self.horizons:
            scale = 1 + (horizon / 120)
            predicted_users = int(round(base_load * scale + load_factor * horizon))
            predicted_requests = int(round(input_data.get("requests_per_second", 0) * scale))
            predicted_volume = round(traffic_volume * scale * (1 + utilization / 100), 2)
            predicted_utilization = min(100.0, round(utilization * scale * 0.95, 2))
            predictions.append(
                {
                    "horizon_minutes": horizon,
                    "predicted_concurrent_users": predicted_users,
                    "predicted_requests_per_second": predicted_requests,
                    "predicted_traffic_volume_mb": predicted_volume,
                    "predicted_network_utilization": predicted_utilization,
                }
            )

        return predictions

    def forecast_from_csv(self, csv_path: str, target_column: str = "concurrent_users") -> Dict[str, object]:
        data = pd.read_csv(csv_path, parse_dates=["timestamp"])
        metrics = self.compare_models(data, target_column)
        selected = self.select_best_model(metrics)
        return {
            "metrics": {name: metric.__dict__ for name, metric in metrics.items()},
            "best_model": selected,
        }
