from typing import List
from fastapi import APIRouter, Query
from app.services.advisory_service import advisory_service
from app.schemas.schemas import AdvisoryDetail

router = APIRouter(prefix="/advisories", tags=["Multilingual Farmer Advisories"])

@router.get("", response_model=List[AdvisoryDetail])
def get_advisories(condition: str = Query("Early Blight")):
    """
    Returns localized farmer advisories in English (en), Hindi (hi), and Telugu (te).
    """
    return advisory_service.generate_advisories(condition)
