from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import PestTrap, TrapObservation
from ml.pest_detection.trap_engine import pest_trap_pipeline
from app.schemas.schemas import PestTrapResponse, PestPredictionResult

router = APIRouter(prefix="/pest", tags=["Pest Trap Surveillance"])

@router.get("/traps", response_model=List[PestTrapResponse])
def list_traps(db: Session = Depends(get_db)):
    traps = db.query(PestTrap).all()
    results = []
    for t in traps:
        latest = db.query(TrapObservation).filter(TrapObservation.trap_id == t.id).order_by(TrapObservation.observation_date.desc()).first()
        results.append({
            "id": t.id,
            "trap_code": t.trap_code,
            "trap_type": t.trap_type,
            "target_pest": t.target_pest,
            "latitude": t.latitude,
            "longitude": t.longitude,
            "is_active": t.is_active,
            "current_count": latest.pest_count if latest else 0,
            "previous_count": latest.previous_count if latest else 0,
            "population_trend": latest.population_trend if latest else "Stable",
            "risk_level": latest.risk_level if latest else "Low",
            "economic_threshold_level": latest.economic_threshold_level if latest else 20,
            "last_observation_date": latest.observation_date if latest else t.installed_at,
            "farm_name": t.farm.name if t.farm else "Farm",
            "village": t.farm.village if t.farm else "Village"
        })
    return results

@router.post("/predict", response_model=PestPredictionResult)
def predict_pest(
    trap_id: Optional[str] = Form("TRAP-102"),
    target_pest: str = Form("Fruit Fly"),
    current_count: Optional[int] = Form(None),
    previous_count: Optional[int] = Form(18),
    image_url: Optional[str] = Form(None)
):
    """
    Executes automated computer vision analysis on pest trap images,
    detects insect specimens, and analyzes population velocity against ETL thresholds.
    """
    analysis = pest_trap_pipeline.analyze_trap(
        trap_id=trap_id,
        target_pest=target_pest,
        current_count=current_count,
        previous_count=previous_count,
        image_path=image_url
    )

    return {
        "trap_id": analysis["trap_id"],
        "pest_species": analysis["scientific_name"],
        "pest_count": analysis["count"],
        "population_trend": analysis["trend"],
        "risk_level": analysis["risk_level"],
        "economic_threshold_level": analysis["economic_threshold_level"],
        "exceeds_etl": analysis["exceeds_etl"],
        "confidence": 0.93,
        "recommendation": analysis["action_guidance"],
        "annotated_image_url": analysis.get("annotated_image_url")
    }
