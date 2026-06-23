# System Architecture

This project implements an AI-driven decision support platform for flash crowd events on university digital platforms.

## Components

- Frontend: Next.js dashboard with KPI monitoring, model comparison, and what-if simulation.
- Backend: FastAPI service exposing endpoints for dataset management, forecasting, congestion, QoE, and QoS recommendations.
- Database: PostgreSQL for dataset metadata, model results, and KPI logs.
- ML Pipelines: Modular training and evaluation for forecasting, classification, resource allocation, QoE prediction, and recommendation.
