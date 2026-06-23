from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI(
    title="AI-Driven Traffic Control and Congestion Management",
    version="0.1.0",
    description="Backend API for forecasting, congestion detection, resource allocation, QoE prediction, and QoS recommendation."
)

app.include_router(api_router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "congestion-control"}
