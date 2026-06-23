#!/bin/bash

# Start the FastAPI backend in the background
echo "Starting FastAPI backend on port 8000..."
cd /app/backend
PYTHONPATH=/app/backend python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# Start the Next.js frontend in the background
echo "Starting Next.js frontend on port ${PORT:-7860}..."
cd /app/frontend
npm run start -- -p ${PORT:-7860} &
FRONTEND_PID=$!

# Handle shutdown signals gracefully
cleanup() {
    echo "Shutting down..."
    kill $BACKEND_PID || true
    kill $FRONTEND_PID || true
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for processes
wait -n $BACKEND_PID $FRONTEND_PID
