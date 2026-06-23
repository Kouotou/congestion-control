from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from app.api.schemas import (
    CongestionPredictionRequest,
    CongestionPredictionResponse,
    DatasetInfoResponse,
    DatasetUploadResponse,
    ForecastComparisonResponse,
    ForecastRequest,
    ForecastResponse,
    ForecastTrainingResponse,
    KPIInfo,
    KPIInteraction,
    QoEPredictionRequest,
    QoEPredictionResponse,
    QoSRecommendationRequest,
    QoSRecommendationResponse,
    ResourceAllocationRequest,
    ResourceAllocationResponse,
    WhatIfRequest,
    WhatIfResponse,
)
from app.services.dataset_service import (
    get_available_datasets,
    get_dataset_info,
    inspect_dataset,
    save_dataset,
    standardize_dataset,
)
from app.services.decision_support import (
    predict_congestion,
    predict_qoe,
    recommend_qos,
    recommend_resource_allocation,
    run_what_if_simulation,
)
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


@router.get("/datasets", response_model=list[DatasetInfoResponse])
def datasets():
    return get_available_datasets()


@router.get("/datasets/{dataset_id}", response_model=DatasetInfoResponse)
def dataset_info(dataset_id: str):
    info = get_dataset_info(dataset_id)
    if info is None:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    return info


@router.post("/forecast", response_model=list[ForecastResponse])
def forecast(request: ForecastRequest):
    return forecast_engine.predict(request.model_dump())


@router.post("/forecast/compare", response_model=ForecastComparisonResponse)
def forecast_compare(dataset_id: str, target_column: str = "concurrent_users"):
    try:
        df = standardize_dataset(dataset_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    comparison = pipeline.train_models(pipeline.prepare_features(df, target_column), target_column)
    metrics = [
        {
            "model_name": name,
            **metric,
        }
        for name, metric in comparison.to_dict().items()
    ]
    return {
        "best_model": comparison.best_model(),
        "metrics": metrics,
    }


@router.post("/forecast/train", response_model=ForecastTrainingResponse)
def forecast_train(dataset_id: str, target_column: str = "concurrent_users"):
    try:
        df = standardize_dataset(dataset_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Dataset not found.")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    training = pipeline.train_models(pipeline.prepare_features(df, target_column), target_column)
    metrics = [
        {
            "model_name": name,
            **metric,
        }
        for name, metric in training.to_dict().items()
    ]
    return {
        "dataset_id": dataset_id,
        "best_model": training.best_model(),
        "metrics": metrics,
        "message": "Forecast models trained and compared successfully.",
    }


@router.post("/congestion", response_model=CongestionPredictionResponse)
def congestion(request: CongestionPredictionRequest):
    return predict_congestion(**request.model_dump())


@router.post("/qoe", response_model=QoEPredictionResponse)
def qoe(request: QoEPredictionRequest):
    return predict_qoe(**request.model_dump())


@router.post("/qos/recommend", response_model=QoSRecommendationResponse)
def qos_recommend(request: QoSRecommendationRequest):
    return recommend_qos(**request.model_dump())


@router.post("/resource-allocation", response_model=ResourceAllocationResponse)
def resource_allocation(request: ResourceAllocationRequest):
    return recommend_resource_allocation(**request.model_dump())


@router.post("/what-if", response_model=WhatIfResponse)
def what_if(request: WhatIfRequest):
    return run_what_if_simulation(request.model_dump())
