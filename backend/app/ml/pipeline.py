from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from app.ml.forecasting import ForecastMetrics, TrafficForecastEngine

try:
    from xgboost import XGBRegressor
except ImportError:
    XGBRegressor = None

try:
    from lightgbm import LGBMRegressor
except ImportError:
    LGBMRegressor = None

try:
    from prophet import Prophet
except ImportError:
    Prophet = None

try:
    from statsmodels.tsa.arima.model import ARIMA
except ImportError:
    ARIMA = None

try:
    from tensorflow.keras.callbacks import EarlyStopping
    from tensorflow.keras.layers import Dense, GRU, LSTM
    from tensorflow.keras.models import Sequential
except ImportError:
    Sequential = None
    LSTM = None
    GRU = None
    Dense = None
    EarlyStopping = None


@dataclass
class ModelScorecard:
    results: Dict[str, ForecastMetrics]

    def __init__(self):
        self.results = {}

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
        self.model_names = [
            "random_forest",
            "xgboost",
            "lightgbm",
            "arima",
            "prophet",
            "lstm",
            "gru",
        ]

    def load_dataset(self, csv_path: str) -> pd.DataFrame:
        df = pd.read_csv(csv_path, parse_dates=["timestamp"])
        if "timestamp" not in df.columns:
            raise ValueError("Dataset requires a 'timestamp' column.")
        return df.sort_values("timestamp").reset_index(drop=True)

    def prepare_features(self, df: pd.DataFrame, target_column: str) -> pd.DataFrame:
        return self.engine._build_lag_features(df, target_column)

    def _split_data(self, X: pd.DataFrame, y: pd.Series) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train.to_numpy(), X_test.to_numpy(), y_train.to_numpy(), y_test.to_numpy()

    def _evaluate(self, y_true: np.ndarray, y_pred: np.ndarray) -> ForecastMetrics:
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mape = np.mean(np.abs((y_true - y_pred) / np.maximum(np.abs(y_true), 1))) * 100
        r2 = r2_score(y_true, y_pred) if len(y_true) > 1 else 0.0
        return ForecastMetrics(mae=mae, rmse=rmse, mape=mape, r2=r2)

    def _train_sklearn(self, model: Any, X_train: np.ndarray, X_test: np.ndarray, y_train: np.ndarray, y_test: np.ndarray) -> ForecastMetrics:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        return self._evaluate(y_test, y_pred)

    def _train_prophet(self, df: pd.DataFrame, target_column: str) -> ForecastMetrics:
        if Prophet is None:
            raise ImportError("Prophet is not available in the environment.")

        n = len(df)
        split = max(3, int(n * 0.8))
        train = df.iloc[:split]
        test = df.iloc[split:]
        if test.empty:
            raise ValueError("Not enough data to train Prophet model.")

        train_df = train[["timestamp", target_column]].rename(columns={"timestamp": "ds", target_column: "y"})
        test_df = test[["timestamp"]].rename(columns={"timestamp": "ds"})

        model = Prophet()
        model.fit(train_df)
        forecast = model.predict(test_df)
        y_pred = forecast["yhat"].values
        return self._evaluate(test[target_column].to_numpy(), y_pred)

    def _train_arima(self, df: pd.DataFrame, target_column: str) -> ForecastMetrics:
        if ARIMA is None:
            raise ImportError("statsmodels ARIMA is not available in the environment.")

        series = df[target_column]
        n = len(series)
        split = max(10, int(n * 0.8))
        train = series.iloc[:split]
        test = series.iloc[split:]
        if test.empty:
            raise ValueError("Not enough data to train ARIMA model.")

        model = ARIMA(train, order=(2, 1, 2))
        fitted = model.fit()
        y_pred = fitted.forecast(steps=len(test))
        return self._evaluate(test.to_numpy(), np.asarray(y_pred))

    def _to_sequence_data(self, X: np.ndarray) -> np.ndarray:
        return X.reshape((X.shape[0], X.shape[1], 1))

    def _build_rnn(self, input_shape: Tuple[int, int], model_type: str) -> Any:
        if Sequential is None or Dense is None or LSTM is None or GRU is None:
            raise ImportError("TensorFlow Keras is not available in the environment.")

        model = Sequential()
        if model_type == "lstm":
            model.add(LSTM(32, activation="tanh", input_shape=input_shape))
        else:
            model.add(GRU(32, activation="tanh", input_shape=input_shape))
        model.add(Dense(1))
        model.compile(optimizer="adam", loss="mse")
        return model

    def _train_rnn(self, X_train: np.ndarray, X_test: np.ndarray, y_train: np.ndarray, y_test: np.ndarray, model_type: str) -> ForecastMetrics:
        X_train_seq = self._to_sequence_data(X_train)
        X_test_seq = self._to_sequence_data(X_test)
        model = self._build_rnn((X_train_seq.shape[1], X_train_seq.shape[2]), model_type)

        callbacks = []
        if EarlyStopping is not None:
            callbacks = [EarlyStopping(monitor="loss", patience=3, restore_best_weights=True)]

        model.fit(X_train_seq, y_train, epochs=20, batch_size=8, verbose=0, callbacks=callbacks)
        y_pred = model.predict(X_test_seq, verbose=0).flatten()
        return self._evaluate(y_test, y_pred)

    def train_models(self, df: pd.DataFrame, target_column: str) -> ModelScorecard:
        scorecard = ModelScorecard()
        features = [col for col in df.columns if col != target_column and col != "timestamp"]
        if not features:
            raise ValueError("No features available for model training.")

        X = df[features]
        y = df[target_column]

        if "prophet" in self.model_names:
            try:
                prophet_metrics = self._train_prophet(df, target_column)
                scorecard.add("prophet", prophet_metrics)
            except Exception:
                pass

        if "arima" in self.model_names:
            try:
                arima_metrics = self._train_arima(df, target_column)
                scorecard.add("arima", arima_metrics)
            except Exception:
                pass

        X_train, X_test, y_train, y_test = self._split_data(X, y)

        if "random_forest" in self.model_names:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            scorecard.add("random_forest", self._train_sklearn(model, X_train, X_test, y_train, y_test))

        if "xgboost" in self.model_names and XGBRegressor is not None:
            model = XGBRegressor(n_estimators=50, random_state=42, verbosity=0)
            scorecard.add("xgboost", self._train_sklearn(model, X_train, X_test, y_train, y_test))

        if "lightgbm" in self.model_names and LGBMRegressor is not None:
            model = LGBMRegressor(n_estimators=50, random_state=42)
            scorecard.add("lightgbm", self._train_sklearn(model, X_train, X_test, y_train, y_test))

        for rnn_type in ["lstm", "gru"]:
            if rnn_type in self.model_names:
                try:
                    scorecard.add(rnn_type, self._train_rnn(X_train, X_test, y_train, y_test, rnn_type))
                except Exception:
                    pass

        if not scorecard.results:
            raise RuntimeError("No forecasting models were successfully trained.")

        return scorecard

    def train_from_csv(self, csv_path: str, target_column: str = "concurrent_users") -> Dict[str, Any]:
        df = self.load_dataset(csv_path)
        prepared = self.prepare_features(df, target_column)
        scorecard = self.train_models(prepared, target_column)
        return {
            "best_model": scorecard.best_model(),
            "metrics": scorecard.to_dict(),
        }
