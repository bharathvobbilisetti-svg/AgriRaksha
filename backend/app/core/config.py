import os
from pathlib import Path
from pydantic_core import Url

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
(DATA_DIR / "sample_images").mkdir(parents=True, exist_ok=True)

class Settings:
    PROJECT_NAME: str = "AgriRaksha — Crop Health Early Warning & Decision Support"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Secret key for JWT & HMAC tokens
    SECRET_KEY: str = os.getenv("SECRET_KEY", "agriraksha-sih2026-hypersecure-session-salt-082490")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days for hackathon convenience
    
    # Database: Default to portable SQLite with fallback to PostgreSQL
    # Example PostgreSQL: postgresql+psycopg2://user:password@localhost:5432/agriraksha
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/agriraksha.db")
    
    # ML & Risk Engine Weights
    WEIGHT_VISUAL: float = 0.35
    WEIGHT_WEATHER: float = 0.25
    WEIGHT_CROP_STAGE: float = 0.15
    WEIGHT_GEO_HISTORY: float = 0.15
    WEIGHT_PEST_PRESSURE: float = 0.10
    
    # GIS Hotspot Proximity Radius (km)
    HOTSPOT_RADIUS_KM: float = 10.0
    CONFIRMED_OUTBREAK_PROXIMITY_KM: float = 5.0

settings = Settings()
