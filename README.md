# AI-Driven Dynamic Traffic Control and Congestion Management

An end-to-end decision support platform for flash crowd events and network congestion control. It combines a FastAPI backend, ML forecasting and decision support logic, and a Next.js frontend dashboard for visualization and interaction.

## What this project does

- Forecasts traffic and user load using historical and current KPI inputs
- Detects congestion probability for flash crowd scenarios
- Predicts QoE from QoS measurements
- Recommends QoS and resource allocation settings
- Supports scenario-based what-if simulation for decision support

## Repository structure

- `backend/` – FastAPI application, API routes, data services, ML pipeline, and decision support logic
- `frontend/` – Next.js dashboard with React and Tailwind CSS
- `data/` – dataset files and staging area
- `docs/` – architecture and deployment documentation
- `notebooks/` – Jupyter notebooks for analysis and model exploration
- `tests/` – Python unit and integration tests

## Prerequisites

- Python 3.11+ or 3.12+
- Node.js 18+ / npm 10+
- Git (for cloning or pushing changes)

## Local setup

### 1. Clone the repository

```powershell
git clone https://github.com/Kouotou/congestion-control.git
cd congestioncontrol
```

### 2. Setup Python backend

```powershell
python -m venv .congestionctrl
.\.congestionctrl\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### 3. Setup frontend

```powershell
cd frontend
npm install
```

## Run the application locally

### 1. Start the backend

From the repository root or the backend folder:

```powershell
cd backend
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend API will be available at `http://localhost:8000`.

### 2. Start the frontend

Open a second terminal and run:

```powershell
cd frontend
npm run dev
```

Frontend dashboard will be available at `http://localhost:3000`.

## How the app is structured

### Backend

- `backend/app/main.py` – FastAPI app entrypoint
- `backend/app/api/routes.py` – API endpoints for datasets, forecast, congestion, QoE, QoS recommendation, and what-if simulation
- `backend/app/api/schemas.py` – Pydantic request/response schemas
- `backend/app/services/` – business logic and data service utilities
- `backend/app/ml/` – forecasting engine and model pipeline

### Frontend

- `frontend/pages/index.js` – dashboard landing page
- `frontend/pages/api/*.js` – proxy routes to the backend API
- `frontend/components/` – dashboard panels and UI widgets
- `frontend/styles/` – global CSS and styling support

## Testing

### Backend tests

From the repository root with the Python venv activated:

```powershell
pytest
```

If tests are scoped to backend packages, you can run:

```powershell
cd backend
pytest
```

### Frontend linting

From `frontend/`:

```powershell
npm run lint
```

## Environment configuration

Use `NEXT_PUBLIC_API_BASE_URL` in the frontend to point to a deployed or alternate backend URL.

Example:

```powershell
$env:NEXT_PUBLIC_API_BASE_URL = 'http://localhost:8000'
npm run dev
```

## Deployment notes

- Ensure the backend is accessible before starting the frontend
- Use a production build for deployment:

```powershell
cd frontend
npm run build
npm run start
```

- In production, set the frontend environment variable to your backend host.

## Useful commands

- `python -m venv .congestionctrl` – create Python virtual environment
- `pip install -r backend/requirements.txt` – install backend packages
- `npm install` – install frontend packages
- `uvicorn backend.app.main:app --reload` – run backend locally
- `npm run dev` – run frontend dashboard locally
- `pytest` – run Python tests

## Contact

If you need help understanding the dashboard or API, open an issue in this repository or review `docs/architecture.md` for deeper design details.
