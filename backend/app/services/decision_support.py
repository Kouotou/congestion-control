import math
from typing import Dict, Optional


def predict_congestion(
    concurrent_users: int,
    requests_per_second: float,
    traffic_volume_mb: float,
    network_utilization: float,
) -> Dict[str, object]:
    score = (
        min(max(network_utilization, 0.0), 100.0) * 0.55
        + min(max(requests_per_second, 0.0), 1000.0) * 0.15
        + min(max(concurrent_users, 0), 1000) * 0.1
        + min(max(traffic_volume_mb, 0.0), 1000.0) * 0.1
    )
    probability = min(1.0, max(0.0, score / 120.0))
    if probability >= 0.75:
        state = "High"
    elif probability >= 0.4:
        state = "Medium"
    else:
        state = "Low"
    return {
        "state": state,
        "probability": round(probability, 3),
    }


def predict_qoe(
    latency_ms: float,
    jitter_ms: float,
    packet_loss_pct: float,
    throughput_mbps: float,
    response_time_ms: float,
    timeout_rate_pct: float,
) -> Dict[str, object]:
    latency_penalty = min(max(latency_ms / 200.0, 0.0), 1.0)
    jitter_penalty = min(max(jitter_ms / 100.0, 0.0), 1.0)
    loss_penalty = min(max(packet_loss_pct / 5.0, 0.0), 1.0)
    response_penalty = min(max(response_time_ms / 500.0, 0.0), 1.0)
    timeout_penalty = min(max(timeout_rate_pct / 10.0, 0.0), 1.0)
    throughput_bonus = min(max(throughput_mbps / 200.0, 0.0), 1.0)

    score = 100.0
    score -= latency_penalty * 25.0
    score -= jitter_penalty * 15.0
    score -= loss_penalty * 25.0
    score -= response_penalty * 20.0
    score -= timeout_penalty * 15.0
    score += throughput_bonus * 20.0

    qoe_score = max(0.0, min(100.0, score))
    if qoe_score >= 80.0:
        satisfaction_level = "Excellent"
    elif qoe_score >= 60.0:
        satisfaction_level = "Good"
    elif qoe_score >= 40.0:
        satisfaction_level = "Fair"
    else:
        satisfaction_level = "Poor"

    return {
        "qoe_score": round(qoe_score, 1),
        "satisfaction_level": satisfaction_level,
    }


def recommend_qos(
    predicted_concurrent_users: int,
    predicted_requests_per_second: float,
    expected_session_duration_minutes: int,
    historical_qos: Optional[Dict[str, object]] = None,
    current_qos: Optional[Dict[str, object]] = None,
) -> Dict[str, object]:
    effective_users = max(1, predicted_concurrent_users)
    effective_requests = max(1.0, predicted_requests_per_second)

    required_throughput_mbps = round(effective_requests * 0.3 + effective_users * 0.1, 2)
    required_bandwidth_gbps = round(max(0.1, required_throughput_mbps / 1000.0 * 1.2), 3)
    maximum_latency_ms = 120.0 if effective_requests < 500 else 180.0
    maximum_jitter_ms = 25.0 if effective_requests < 500 else 40.0
    maximum_packet_loss_pct = 0.5 if effective_requests < 500 else 1.0
    required_queue_length = min(2000, max(10, math.ceil(effective_requests * 0.25)))
    required_cpu_pct = min(95.0, max(25.0, effective_users * 0.08))
    required_memory_gb = round(max(1.0, effective_users * 0.025 + required_throughput_mbps * 0.01), 2)
    required_servers = max(1, math.ceil(effective_users / 150))

    qoe_score = predict_qoe(
        latency_ms=maximum_latency_ms,
        jitter_ms=maximum_jitter_ms,
        packet_loss_pct=maximum_packet_loss_pct,
        throughput_mbps=required_throughput_mbps,
        response_time_ms=maximum_latency_ms,
        timeout_rate_pct=0.5,
    )["qoe_score"]

    note_parts = [
        "Provision capacity proactively for the predicted load.",
        "Use traffic shaping and session pacing to keep latency below thresholds.",
    ]
    if historical_qos or current_qos:
        note_parts.append("Compare recommendations with observed QoS metrics for fine tuning.")

    return {
        "expected_users": effective_users,
        "required_bandwidth_gbps": required_bandwidth_gbps,
        "required_throughput_mbps": required_throughput_mbps,
        "maximum_latency_ms": maximum_latency_ms,
        "maximum_jitter_ms": maximum_jitter_ms,
        "maximum_packet_loss_pct": maximum_packet_loss_pct,
        "required_queue_length": required_queue_length,
        "required_cpu_pct": required_cpu_pct,
        "required_memory_gb": required_memory_gb,
        "required_servers": required_servers,
        "predicted_qoe_score": round(qoe_score, 1),
        "notes": " ".join(note_parts),
    }


def recommend_resource_allocation(
    predicted_concurrent_users: int,
    predicted_requests_per_second: float,
    expected_session_duration_minutes: int,
) -> Dict[str, object]:
    effective_users = max(1, predicted_concurrent_users)
    effective_requests = max(1.0, predicted_requests_per_second)
    throughput_mbps = round(effective_requests * 0.3 + effective_users * 0.1, 2)
    cpu_needed = min(95.0, max(20.0, effective_users * 0.07 + effective_requests * 0.02))
    memory_needed = round(max(1.0, effective_users * 0.02 + throughput_mbps * 0.008), 2)
    servers = max(1, math.ceil(effective_users / 160))
    latency_target = 120.0 if effective_requests < 500 else 170.0

    return {
        "required_servers": servers,
        "required_cpu_pct": round(cpu_needed, 1),
        "required_memory_gb": memory_needed,
        "required_bandwidth_gbps": round(max(0.1, throughput_mbps / 1000.0 * 1.1), 3),
        "required_throughput_mbps": throughput_mbps,
        "expected_users": effective_users,
        "latency_target_ms": latency_target,
        "notes": "Allocate resources to maintain latency targets and keep CPU below 90%.",
    }


def run_what_if_simulation(payload: Dict[str, object]) -> Dict[str, object]:
    forecast_input = {
        "concurrent_users": int(payload.get("concurrent_users", 0)),
        "requests_per_second": float(payload.get("requests_per_second", 0.0)),
        "traffic_volume_mb": float(payload.get("traffic_volume_mb", 0.0)),
        "network_utilization": float(payload.get("network_utilization", 0.0)),
    }
    congestion_result = predict_congestion(
        concurrent_users=forecast_input["concurrent_users"],
        requests_per_second=forecast_input["requests_per_second"],
        traffic_volume_mb=forecast_input["traffic_volume_mb"],
        network_utilization=forecast_input["network_utilization"],
    )
    qoe_result = predict_qoe(
        latency_ms=float(payload.get("latency_ms", 50.0)),
        jitter_ms=float(payload.get("jitter_ms", 10.0)),
        packet_loss_pct=float(payload.get("packet_loss_pct", 0.1)),
        throughput_mbps=float(payload.get("throughput_mbps", 20.0)),
        response_time_ms=float(payload.get("response_time_ms", 100.0)),
        timeout_rate_pct=float(payload.get("timeout_rate_pct", 0.5)),
    )
    qos_result = recommend_qos(
        predicted_concurrent_users=forecast_input["concurrent_users"],
        predicted_requests_per_second=forecast_input["requests_per_second"],
        expected_session_duration_minutes=int(payload.get("expected_session_duration_minutes", 30)),
        historical_qos=payload.get("historical_qos"),
        current_qos=payload.get("current_qos"),
    )

    return {
        "forecast_input": forecast_input,
        "congestion": congestion_result,
        "qoe": qoe_result,
        "qos_recommendation": qos_result,
    }
