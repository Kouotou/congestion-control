import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

DATA_DIR = Path("./data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

KNOWN_DATASETS = [
    {
        "dataset_id": "weblog",
        "filename": "weblog.csv",
        "name": "Web Traffic Log",
        "description": "Web server access logs for user traffic and session activity.",
        "dataset_type": "weblog",
    },
    {
        "dataset_id": "telecom_qos",
        "filename": "6G_network_slicing_qos_dataset_2345.csv",
        "name": "Telecom QoS KPI Dataset",
        "description": "6G network slicing QoS measurements and traffic load metrics.",
        "dataset_type": "telecom_qos",
    },
]


def save_dataset(file_name: str, contents: bytes) -> Dict[str, str]:
    dataset_id = str(uuid.uuid4())
    target_path = DATA_DIR / f"{dataset_id}_{file_name}"
    target_path.write_bytes(contents)
    return {"dataset_id": dataset_id, "path": str(target_path)}


def inspect_dataset(file_path: str) -> Dict[str, Any]:
    df = pd.read_csv(file_path)
    schema = {col: str(dtype) for col, dtype in zip(df.columns, df.dtypes)}
    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "schema": schema,
    }


def get_available_datasets() -> List[Dict[str, Any]]:
    results = []
    for dataset in KNOWN_DATASETS:
        path = DATA_DIR / dataset["filename"]
        if path.exists():
            metadata = inspect_dataset(str(path))
            results.append(
                {
                    **dataset,
                    "path": str(path),
                    "row_count": metadata["row_count"],
                    "column_count": metadata["column_count"],
                    "columns": list(metadata["schema"].keys()),
                }
            )
    return results


def get_dataset_info(dataset_id: str) -> Optional[Dict[str, Any]]:
    dataset = next((item for item in KNOWN_DATASETS if item["dataset_id"] == dataset_id), None)
    if dataset is None:
        return None

    path = DATA_DIR / dataset["filename"]
    if not path.exists():
        return None

    metadata = inspect_dataset(str(path))
    return {
        **dataset,
        "path": str(path),
        "row_count": metadata["row_count"],
        "column_count": metadata["column_count"],
        "columns": list(metadata["schema"].keys()),
    }


def load_dataset_by_id(dataset_id: str) -> pd.DataFrame:
    info = get_dataset_info(dataset_id)
    if info is None:
        raise FileNotFoundError(f"Dataset {dataset_id} not found.")
    return pd.read_csv(info["path"])


def _standardize_weblog(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "Time" not in df.columns or "IP" not in df.columns:
        raise ValueError("Weblog dataset missing required Time or IP columns.")

    df["Time"] = df["Time"].astype(str).str.strip("[]")
    df["timestamp"] = pd.to_datetime(df["Time"], format="%d/%b/%Y:%H:%M:%S", errors="coerce")
    df = df.dropna(subset=["timestamp"]) 
    df["request_count"] = 1
    grouped = (
        df.groupby(pd.Grouper(key="timestamp", freq="1min"))
        .agg(
            concurrent_users=("IP", "nunique"),
            requests=("request_count", "sum"),
        )
        .reset_index()
    )
    grouped["requests_per_second"] = grouped["requests"] / 60.0
    grouped["traffic_volume_mb"] = grouped["requests"] * 0.05
    grouped["network_utilization"] = (grouped["requests_per_second"] / grouped["requests_per_second"].max()).fillna(0) * 100
    return grouped[["timestamp", "concurrent_users", "requests_per_second", "traffic_volume_mb", "network_utilization"]]


def _standardize_telecom_qos(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "Timestamp" not in df.columns or "Traffic Load (bps)" not in df.columns:
        raise ValueError("Telecom QoS dataset missing required Timestamp or Traffic Load columns.")

    df["timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"]) 
    df["concurrent_users"] = (df["Traffic Load (bps)"] / 1e5).round().astype(int)
    df["requests_per_second"] = df.get("QoS Metric (Throughput)", df.get("Bandwidth Utilization (%)", 0)) * 10
    df["traffic_volume_mb"] = (df["Traffic Load (bps)"] / 8 / 1e6 * 60).round(3)
    df["network_utilization"] = (df["Network Utilization (%)"].fillna(0) * 100).clip(0, 100)
    return df[["timestamp", "concurrent_users", "requests_per_second", "traffic_volume_mb", "network_utilization"]]


def standardize_dataset(dataset_id: str, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    if df is None:
        df = load_dataset_by_id(dataset_id)

    if dataset_id == "weblog":
        return _standardize_weblog(df)
    if dataset_id == "telecom_qos":
        return _standardize_telecom_qos(df)

    raise ValueError(f"Unsupported dataset type: {dataset_id}")
