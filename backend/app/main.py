import os
import sys
from pathlib import Path

# Add repository root to sys.path so ml module is always discoverable
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings, UPLOAD_DIR
from app.db.session import engine, Base
from app.api import (
    auth, farms, disease, pest, weather,
    risk, hotspots, cases, expert, ipm,
    advisories, dashboard, demo
)

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="""
    ## AgriRaksha — AI-Powered Crop Health Early Warning & Decision Support System (SIH 2026)
    
    A multimodal crop-health intelligence platform integrating:
    * **Visual Leaf Pathology & Symptom Detection**
    * **Pest-Trap Computer Vision & Economic Threshold Surveillance**
    * **Microclimate Weather Disease Suitability Modeling**
    * **Geospatial Hotspot Clustering & Epidemiological Buffer Zones**
    * **Human Expert Agronomist Validation & Continuous Learning Feedback**
    * **Tiered Integrated Pest Management (IPM) & Non-Fabricated Safety Guidance**
    * **Multilingual Farmer Advisories (English, Hindi, Telugu)**
    * **Longitudinal Case Follow-Up & Epidemic Progression Forecasting**
    """
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import FileResponse
from pathlib import Path

# Mount uploads directory
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# Mount frontend dist static assets if built
FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="frontend-assets")

# Include Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(farms.router, prefix=settings.API_V1_STR)
app.include_router(disease.router, prefix=settings.API_V1_STR)
app.include_router(pest.router, prefix=settings.API_V1_STR)
app.include_router(weather.router, prefix=settings.API_V1_STR)
app.include_router(risk.router, prefix=settings.API_V1_STR)
app.include_router(hotspots.router, prefix=settings.API_V1_STR)
app.include_router(cases.router, prefix=settings.API_V1_STR)
app.include_router(expert.router, prefix=settings.API_V1_STR)
app.include_router(ipm.router, prefix=settings.API_V1_STR)
app.include_router(advisories.router, prefix=settings.API_V1_STR)
app.include_router(dashboard.router, prefix=settings.API_V1_STR)
app.include_router(demo.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    index_file = FRONTEND_DIST / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {
        "platform": "AgriRaksha (SIH 2026)",
        "status": "online",
        "docs_url": "/docs",
        "api_prefix": settings.API_V1_STR
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "engine": "FastAPI", "version": settings.PROJECT_VERSION}
