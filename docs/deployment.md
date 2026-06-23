# Deployment Guide

## Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL
- Docker (optional)

## Backend

1. Create virtual environment:

   ```powershell
   python -m venv .congestionctrl
   .\.congestionctrl\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r backend/requirements.txt
   ```

3. Start PostgreSQL and create database `congestiondb`.

4. Run backend:

   ```powershell
   uvicorn backend.app.main:app --reload
   ```

## Frontend

1. Install dependencies:

   ```powershell
   cd frontend
   npm install
   npm run dev
   ```

## Docker

Add Docker Compose support in a later iteration.
