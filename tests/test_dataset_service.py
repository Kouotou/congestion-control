import pandas as pd

from app.services.dataset_service import (
    get_available_datasets,
    get_dataset_info,
    load_dataset_by_id,
    standardize_dataset,
)


def test_get_available_datasets_returns_known_items(tmp_path, monkeypatch):
    weblog_csv = tmp_path / "weblog.csv"
    weblog_df = pd.DataFrame(
        {
            "IP": ["1.1.1.1", "2.2.2.2"],
            "Time": ["07/Nov/2017:23:59:00", "08/Nov/2017:00:00:00"],
            "URL": ["/index", "/about"],
            "Staus": ["200", "200"],
        }
    )
    weblog_df.to_csv(weblog_csv, index=False)

    telecom_csv = tmp_path / "6G_network_slicing_qos_dataset_2345.csv"
    telecom_df = pd.DataFrame(
        {
            "Timestamp": ["2025-01-01 00:00:00", "2025-01-01 01:00:00"],
            "Traffic Load (bps)": [1000000, 2000000],
            "Network Utilization (%)": [0.5, 0.6],
            "QoS Metric (Throughput)": [10, 20],
        }
    )
    telecom_df.to_csv(telecom_csv, index=False)

    monkeypatch.setattr("app.services.dataset_service.DATA_DIR", tmp_path)

    datasets = get_available_datasets()
    dataset_ids = {item["dataset_id"] for item in datasets}
    assert {"weblog", "telecom_qos"}.issubset(dataset_ids)


def test_get_dataset_info_and_load(tmp_path, monkeypatch):
    weblog_csv = tmp_path / "weblog.csv"
    weblog_df = pd.DataFrame(
        {
            "IP": ["1.1.1.1", "2.2.2.2"],
            "Time": ["07/Nov/2017:23:59:00", "08/Nov/2017:00:00:00"],
            "URL": ["/index", "/about"],
            "Staus": ["200", "200"],
        }
    )
    weblog_df.to_csv(weblog_csv, index=False)

    monkeypatch.setattr("app.services.dataset_service.DATA_DIR", tmp_path)

    info = get_dataset_info("weblog")
    assert info is not None
    assert info["dataset_id"] == "weblog"
    assert info["row_count"] == 2
    assert "Time" in info["columns"]

    loaded = load_dataset_by_id("weblog")
    assert loaded.shape[0] == 2
    assert loaded["IP"].iloc[0] == "1.1.1.1"


def test_standardize_weblog_data(tmp_path, monkeypatch):
    weblog_csv = tmp_path / "weblog.csv"
    weblog_df = pd.DataFrame(
        {
            "IP": ["1.1.1.1", "1.1.1.1", "2.2.2.2"],
            "Time": ["07/Nov/2017:23:59:00", "07/Nov/2017:23:59:30", "08/Nov/2017:00:00:00"],
            "URL": ["/index", "/api", "/about"],
            "Staus": ["200", "200", "200"],
        }
    )
    weblog_df.to_csv(weblog_csv, index=False)
    monkeypatch.setattr("app.services.dataset_service.DATA_DIR", tmp_path)

    standardized = standardize_dataset("weblog")
    assert "timestamp" in standardized.columns
    assert "concurrent_users" in standardized.columns
    assert standardized.shape[0] == 2
    assert standardized["requests_per_second"].ge(0).all()
    assert int(standardized["concurrent_users"].iloc[0]) == 1


def test_standardize_telecom_qos_data(tmp_path, monkeypatch):
    telecom_csv = tmp_path / "6G_network_slicing_qos_dataset_2345.csv"
    telecom_df = pd.DataFrame(
        {
            "Timestamp": ["2025-01-01 00:00:00", "2025-01-01 01:00:00"],
            "Traffic Load (bps)": [1000000, 2000000],
            "Network Utilization (%)": [0.55, 0.65],
            "QoS Metric (Throughput)": [10, 20],
        }
    )
    telecom_df.to_csv(telecom_csv, index=False)
    monkeypatch.setattr("app.services.dataset_service.DATA_DIR", tmp_path)

    standardized = standardize_dataset("telecom_qos")
    assert "timestamp" in standardized.columns
    assert "concurrent_users" in standardized.columns
    assert standardized["requests_per_second"].iloc[0] == 100
    assert round(float(standardized["network_utilization"].iloc[0]), 6) == 55.0
    assert standardized["concurrent_users"].iloc[0] == 10
