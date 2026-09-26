from typing import List, Dict, Any
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.gis_service import gis_service

router = APIRouter(prefix="/hotspots", tags=["Geospatial Hotspots & GIS Intelligence"])

@router.get("/geojson")
def get_hotspots_geojson(db: Session = Depends(get_db)):
    """
    Returns standard GeoJSON FeatureCollection of all active cases,
    disease clusters, and pest traps for Leaflet visualization.
    """
    return gis_service.generate_hotspots_geojson(db)

@router.get("/clusters")
def get_village_hotspot_clusters(db: Session = Depends(get_db)):
    """
    Returns ranked village-level disease hotspot clusters with metrics.
    """
    return gis_service.get_village_clusters(db)

@router.get("/nearby")
def get_nearby_alerts(
    lat: float = Query(17.6868),
    lon: float = Query(83.2185),
    radius_km: float = Query(5.0),
    db: Session = Depends(get_db)
):
    """
    Returns confirmed cases and active risks within specified radius of a farmer's location.
    """
    cases = gis_service.get_nearby_confirmed_cases(db, lat, lon, radius_km)
    return {
        "latitude": lat,
        "longitude": lon,
        "search_radius_km": radius_km,
        "confirmed_outbreaks_count": len(cases),
        "cases": [
            {
                "case_number": c.case_number,
                "crop": c.crop.name if c.crop else "Unknown",
                "condition": c.confirmed_condition or c.ai_predicted_condition,
                "severity": c.estimated_severity,
                "risk_score": c.multimodal_risk_score,
                "village": c.farm.village,
                "mandal": c.farm.mandal
            }
            for c in cases[:10]
        ]
    }
