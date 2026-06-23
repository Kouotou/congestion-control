import os
from pathlib import Path

import pandas as pd

from app.ml.pipeline import ForecastPipeline


def test_forecast_pipeline_train(tmp_path):
    csv_path = tmp_path / "traffic.csv"
    df = pd.DataFrame(
        {
            "timestamp": pd.date_range(start="2026-01-01", periods=20, freq="5min"),
            "concurrent_users": range(100, 120),
            "requests_per_second": [10 + i * 0.1 for i in range(20)],
            "traffic_volume_mb": [50 + i * 1.5 for i in range(20)],
            "network_utilization": [40 + i * 0.5 for i in range(20)],
        }
    )
    df.to_csv(csv_path, index=False)

    pipeline = ForecastPipeline(model_dir=str(tmp_path / "models"))
    result = pipeline.train_from_csv(str(csv_path), target_column="concurrent_users")

    assert "best_model" in result
    assert result["best_model"] == "random_forest"
    assert "metrics" in result
    assert isinstance(result["metrics"], dict)

    metric_values = next(iter(result["metrics"].values()))
    assert metric_values["mae"] >= 0
    assert metric_values["rmse"] >= 0
