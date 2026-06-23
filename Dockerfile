# Stage 1: Build Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# Stage 2: Runner (Python + Node.js runtime)
FROM python:3.11-slim
WORKDIR /app

# Install Node.js runtime and basic utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends \
    nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy frontend build and package files
COPY --from=frontend-builder /app/frontend /app/frontend

# Copy backend application
COPY backend /app/backend

# Copy initial data (pre-load weblog.csv into data/ directory)
RUN mkdir -p /app/data
COPY weblog.csv /app/data/weblog.csv

# Copy startup script
COPY start.sh /app/start.sh
RUN sed -i 's/\r$//' /app/start.sh && chmod +x /app/start.sh

# Environment variables
ENV PORT=7860
ENV PYTHONPATH=/app/backend
ENV NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000

# Expose port
EXPOSE 7860

# Start services
CMD ["/app/start.sh"]
