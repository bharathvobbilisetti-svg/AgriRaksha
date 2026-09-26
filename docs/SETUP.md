# Setup & Installation Guide — AgriRaksha (SIH 2026)

This document provides step-by-step instructions for running the complete AgriRaksha platform locally on **Windows**, **Linux**, or **macOS**.

---

## 📋 System Prerequisites

1. **Python**: Version 3.8, 3.9, 3.10, or 3.11
2. **Node.js**: Version 18+ & npm 9+
3. **Database**: No external database install required for development/demo (uses embedded SQLite with high-precision haversine geospatial indexing). For production, PostgreSQL 14+ with PostGIS is supported via `DATABASE_URL`.

---

## 🛠️ Step-by-Step Installation

### 1. Clone the Repository
```bash
git clone https://github.com/agriraksha/agriraksha.git
cd agriraksha
```

### 2. Backend Environment Setup
```bash
cd backend

# (Optional) Create and activate virtual environment
python -m venv venv

# Windows (PowerShell / CMD)
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt
```

### 3. Frontend Environment Setup
```bash
cd ../frontend

# Install npm dependencies
npm install

# Build production assets (pre-compiled)
npm run build
```

---

## 🚀 Running the Application

### Option A: One-Click Launch (Windows)
Double-click `scripts\run_all.bat` from File Explorer, or execute:
```cmd
scripts\run_all.bat
```
This automatically boots both the FastAPI backend and React frontend.

### Option B: Manual Multi-Terminal Launch

#### Terminal 1 — FastAPI Backend (Port 8000):
```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
*Backend API will be active at:* `http://127.0.0.1:8000`  
*Swagger Documentation:* `http://127.0.0.1:8000/docs`

#### Terminal 2 — React Frontend (Port 3000):
```bash
cd frontend
npm run dev
```
*Frontend Portal will be active at:* `http://localhost:3000`

---

## 🔄 One-Click Demo Data Seeding

Once the application is running:
1. Open `http://localhost:3000` in any web browser.
2. Click the green **"Load Demo Dataset"** button on the top right of the navigation bar.
3. The system will seed:
   - **105 monitored farms** across 7 villages in Warangal district, Telangana.
   - **25 smart pest surveillance traps** (including `TRAP-102` with 37 Fruit Flies).
   - **6 confirmed Early Blight outbreak cases** clustered in Geesugonda.
   - The primary demo scenario case `AGR-2026-TOM-01`.

Or run the automated script directly:
```bash
python scripts/run_demo_scenario.py
```

---

## 🧪 Running Automated Tests

Execute the full backend test suite:
```bash
python -m pytest backend/tests/ -v
```
All 14 test cases verify authentication, vision adapters, pest trap calculations, multimodal risk fusion, GIS GeoJSON features, and IPM recommendations.
