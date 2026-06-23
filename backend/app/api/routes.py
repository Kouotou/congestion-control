from pathlib import Path

from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from app.api.schemas import (
    KPIInfo,
    KPIInteraction,
    DatasetUploadResponse,
    ForecastRequest,
    ForecastResponse,
    ForecastComparisonResponse,
    ForecastTrainingResponse,
)
from app.services.dataset_service import inspect_dataset, save_dataset
from app.services.kpi_definitions import get_kpi_definitions, get_kpi_interactions
from app.ml.forecasting import TrafficForecastEngine
from app.ml.pipeline import ForecastPipeline

router = APIRouter()

forecast_engine = TrafficForecastEngine()
pipeline = ForecastPipeline()


class HealthResponse(BaseModel):
    status: str
    service: str


@router.get("/ping", response_model=HealthResponse)
def ping():
    return {"status": "ok", "service": "congestion-control"}


@router.post("/datasets/upload", response_model=DatasetUploadResponse)
async def upload_dataset(file: UploadFile = File(...)):
    if file.content_type not in {"text/csv", "application/vnd.ms-excel"}:
        raise HTTPException(status_code=400, detail="Only CSV uploads are supported.")

    contents = await file.read()
    saved = save_dataset(file.filename, contents)
    metadata = inspect_dataset(saved["path"])

    return {
        "dataset_id": saved["dataset_id"],
        "filename": file.filename,
        "row_count": metadata["row_count"],
        "column_count": metadata["column_count"],
        "schema": metadata["schema"],
        "message": "Dataset uploaded and inspected successfully.",
    }


@router.get("/kpis", response_model=list[KPIInfo])
def kpis():
    return get_kpi_definitions()


@router.get("/kpis/interactions", response_model=list[KPIInteraction])
def kpi_interactions():
    return get_kpi_interactions()


@router.post("/forecast", response_model=list[ForecastResponse])
def forecast(request: ForecastRequest):
    return forecast_engine.predict(request.model_dump())


@router.post("/forecast/compare", response_model=ForecastComparisonResponse)
def forecast_compare(dataset_id: str, target_column: str = "concurrent_users"):
    dataset_path = next(
        (str(path) for path in Path("./data").glob(f"{dataset_id}_*.csv")), None
    )
    if dataset_path is None:
        raise HTTPException(status_code=404, detail="Dataset not found.")

    comparison = pipeline.train_from_csv(dataset_path, target_column=target_column)
    metrics = [
        {
            "model_name": name,
            **metric,
        }
        for name, metric in comparison["metrics"].items()
    ]
    return {
        "best_model": comparison["best_model"],
        "metrics": metrics,
    }


@router.post("/forecast/train", response_model=ForecastTrainingResponse)
def forecast_train(dataset_id: str, target_column: str = "concurrent_users"):
    dataset_path = next(
        (str(path) for path in Path("./data").glob(f"{dataset_id}_*.csv")), None
    )
    if dataset_path is None:
        raise HTTPException(status_code=404, detail="Dataset not found.")

    training = pipeline.train_from_csv(dataset_path, target_column=target_column)
    metrics = [
        {
            "model_name": name,
            **metric,
        }
        for name, metric in training["metrics"].items()
    ]
    return {
        "dataset_id": dataset_id,
        "best_model": training["best_model"],
        "metrics": metrics,
        "message": "Forecast models trained and compared successfully.",
    }
