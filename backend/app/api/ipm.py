from fastapi import APIRouter, Query
from app.services.ipm_service import ipm_service
from app.schemas.schemas import IPMDetail

router = APIRouter(prefix="/ipm", tags=["Integrated Pest Management (IPM)"])

@router.get("/recommendations", response_model=IPMDetail)
def get_ipm_recommendations(condition: str = Query("Early Blight")):
    """
    Returns non-chemical first Integrated Pest Management recommendations
    including cultural, mechanical, biological, safety precautions,
    and statutory CIB&RC label guidance.
    """
    return ipm_service.get_recommendation(condition)
