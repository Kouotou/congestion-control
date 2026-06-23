from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DatasetUploadResponse(BaseModel):
    dataset_id: str
    filename: str
    row_count: int
    column_count: int
    schema: Dict[str, str]
    message: str


class DatasetInfoResponse(BaseModel):
    dataset_id: str
    filename: str
    name: str
    description: str
    dataset_type: str
    row_count: int
    column_count: int
    columns: List[str]
    path: str


class KPIInfo(BaseModel):
    name: str
    description: str
    acceptable_range: str
    critical_threshold: str
    qoe_impact: str


class KPIInteraction(BaseModel):
    source: str
    target: str
    relationship: str
    description: str


class ForecastRequest(BaseModel):
    timestamp: str
    concurrent_users: int
    requests_per_second: int
    traffic_volume_mb: float
    network_utilization: float


class ForecastResponse(BaseModel):
    horizon_minutes: int
    predicted_concurrent_users: int
    predicted_requests_per_second: int
    predicted_traffic_volume_mb: float
    predicted_network_utilization: float


class ForecastComparisonResult(BaseModel):
    model_name: str
    mae: float
    rmse: float
    mape: float
    r2: float


class ForecastComparisonResponse(BaseModel):
    best_model: str
    metrics: List[ForecastComparisonResult]


class ForecastTrainingResponse(BaseModel):
    dataset_id: str
    best_model: str
    metrics: List[ForecastComparisonResult]
    message: str


class CongestionPredictionRequest(BaseModel):
    concurrent_users: int
    requests_per_second: int
    traffic_volume_mb: float
    network_utilization: float


class CongestionPredictionResponse(BaseModel):
    state: str
    probability: float


class QoEPredictionRequest(BaseModel):
    latency_ms: float
    jitter_ms: float
    packet_loss_pct: float
    throughput_mbps: float
    response_time_ms: float
    timeout_rate_pct: float


class QoEPredictionResponse(BaseModel):
    qoe_score: float
    satisfaction_level: str


class QoSRecommendationRequest(BaseModel):
    predicted_concurrent_users: int
    predicted_requests_per_second: int
    expected_session_duration_minutes: int
    historical_qos: Optional[Dict[str, Any]] = None
    current_qos: Optional[Dict[str, Any]] = None


class QoSRecommendationResponse(BaseModel):
    expected_users: int
    required_bandwidth_gbps: float
    required_throughput_mbps: float
    maximum_latency_ms: float
    maximum_jitter_ms: float
    maximum_packet_loss_pct: float
    required_queue_length: int
    required_cpu_pct: float
    required_memory_gb: float
    required_servers: int
    predicted_qoe_score: float
    notes: Optional[str] = None
