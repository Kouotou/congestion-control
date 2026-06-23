from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from app.api.schemas import KPIInfo, KPIInteraction, DatasetUploadResponse
from app.services.dataset_service import inspect_dataset, save_dataset
from app.services.kpi_definitions import get_kpi_definitions, get_kpi_interactions

router = APIRouter()


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
