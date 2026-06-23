# AI-Driven Dynamic Traffic Control and Congestion Management

A university-focused end-to-end decision support platform for flash crowd events, traffic forecasting, congestion detection, resource allocation, QoE prediction, and QoS recommendations.

## Workspace Structure

- `backend/` – FastAPI service, ML pipelines, database integration
- `frontend/` – Next.js dashboard with TailwindCSS
- `data/` – Dataset uploads and staging (empty placeholder)
- `notebooks/` – exploratory ML notebooks and methodology
- `docs/` – architecture, deployment guide, reports
- `tests/` – unit and integration tests
- `.congestionctrl/` – Python virtual environment root

## Setup

1. Create or activate the Python virtual environment in the workspace root:

   ```powershell
   python -m venv .congestionctrl
   .\.congestionctrl\Scripts\Activate.ps1
   ```

2. Install backend dependencies:

   ```powershell
   pip install -r backend/requirements.txt
   ```

3. Install frontend dependencies from `frontend/`.

4. Start the backend service:

   ```powershell
   uvicorn backend.app.main:app --reload
   ```

5. Start the frontend app from `frontend/`.

## Project Phases

1. Traffic Forecasting
2. Congestion Detection
3. Dynamic Resource Allocation
4. QoE Prediction
5. QoS Recommendation Engine

## Notes

- Modular dataset upload and retraining support is planned.
- A full CI/CD pipeline and Docker support are included.
