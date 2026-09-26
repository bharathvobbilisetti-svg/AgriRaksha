import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app
from app.db.session import SessionLocal
from app.services.demo_seeder import seed_complete_sih_demo_data

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    db = SessionLocal()
    seed_complete_sih_demo_data(db)
    db.close()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_auth_login():
    response = client.post("/api/auth/login", json={
        "email": "farmer@agriraksha.in",
        "password": "farmer123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["role"] == "farmer"

def test_switch_role():
    response = client.post("/api/auth/switch-role/official")
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["role"] == "official"

def test_get_crop_catalog():
    response = client.get("/api/farms/crops")
    assert response.status_code == 200
    crops = response.json()
    assert len(crops) >= 4
    crop_names = [c["name"] for c in crops]
    assert "Tomato" in crop_names

def test_weather_endpoint():
    response = client.get("/api/weather?lat=17.6868&lon=83.2185")
    assert response.status_code == 200
    data = response.json()
    assert "temperature_c" in data
    assert "relative_humidity_pct" in data
    assert data["relative_humidity_pct"] > 70.0

def test_disease_prediction():
    response = client.post("/api/disease/predict", data={
        "crop_name": "Tomato",
        "image_url": "sample_tomato_early_blight.jpg",
        "symptom_notes": "Concentric rings on lower leaves"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_condition"] == "Early Blight"
    assert data["confidence"] == 0.87
    assert data["needs_expert_validation"] is True
    assert data["is_confirmed"] is False

def test_pest_prediction():
    response = client.post("/api/pest/predict", data={
        "trap_id": "TRAP-102",
        "target_pest": "Fruit Fly",
        "current_count": 37,
        "previous_count": 18
    })
    assert response.status_code == 200
    data = response.json()
    assert data["pest_count"] == 37
    assert data["population_trend"] == "Increasing"
    assert data["risk_level"] == "High"
    assert data["exceeds_etl"] is True

def test_multimodal_risk_calculation():
    response = client.post("/api/risk/calculate", data={
        "crop_name": "Tomato",
        "condition_name": "Early Blight",
        "ai_confidence": 0.87,
        "latitude": 17.6868,
        "longitude": 83.2185,
        "crop_stage_multiplier": 1.4
    })
    assert response.status_code == 200
    data = response.json()
    assert data["final_score"] == 78.0
    assert data["risk_tier"] == "High"
    assert len(data["factors_explanation"]) >= 4

def test_gis_hotspots_geojson():
    response = client.get("/api/hotspots/geojson")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) > 10

def test_expert_review_submission():
    # Submit review on primary case
    response = client.post("/api/expert/review?expert_id=2", json={
        "case_id": 7,  # Primary case
        "confirmed_condition": "Early Blight",
        "diagnostic_agreement": "Confirmed",
        "expert_severity": "Moderate",
        "advisory_notes": "Field inspection confirmed Alternaria solani. Recommended immediate bio-fungicide treatment.",
        "recommend_field_visit": True,
        "recommend_lab_test": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["confirmed_condition"] == "Early Blight"
    assert data["diagnostic_agreement"] == "Confirmed"

def test_ipm_recommendations_and_disclaimer():
    response = client.get("/api/ipm/recommendations?condition=Early Blight")
    assert response.status_code == 200
    data = response.json()
    assert "cultural_control" in data
    assert "biological_control" in data
    assert "safety_precautions" in data
    assert data["extension_consultation_advised"] is True
    assert "CIB&RC" in data["official_disclaimer"]

def test_multilingual_advisories():
    response = client.get("/api/advisories?condition=Early Blight")
    assert response.status_code == 200
    advisories = response.json()
    langs = [a["language_code"] for a in advisories]
    assert "en" in langs
    assert "hi" in langs
    assert "te" in langs

def test_dashboard_statistics():
    response = client.get("/api/dashboard/statistics")
    assert response.status_code == 200
    data = response.json()
    assert data["total_monitored_farms"] >= 100
    assert data["confirmed_outbreaks"] >= 6
    assert len(data["forecast_next_7_days"]) == 7

def test_ml_evaluation_metrics():
    response = client.get("/api/demo/evaluation-metrics")
    assert response.status_code == 200
    data = response.json()
    assert data["accuracy"] > 0.85
    assert "confusion_matrix" in data
    assert "f1_macro" in data
