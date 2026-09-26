from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Farm, CropCatalog, CropStage, CropVariety, FarmerCrop, User
from app.schemas.schemas import FarmCreate, FarmResponse, CropCatalogResponse

router = APIRouter(prefix="/farms", tags=["Farms & Crop Phenology"])

@router.get("", response_model=List[FarmResponse])
def list_farms(farmer_id: int = None, limit: int = 50, db: Session = Depends(get_db)):
    query = db.query(Farm)
    if farmer_id:
        query = query.filter(Farm.farmer_id == farmer_id)
    return query.limit(limit).all()

@router.post("", response_model=FarmResponse)
def create_farm(farm_in: FarmCreate, farmer_id: int = 1, db: Session = Depends(get_db)):
    farmer = db.query(User).filter(User.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
        
    farm = Farm(
        farmer_id=farmer_id,
        name=farm_in.name,
        latitude=farm_in.latitude,
        longitude=farm_in.longitude,
        village=farm_in.village,
        mandal=farm_in.mandal,
        district=farm_in.district,
        state=farm_in.state,
        soil_type=farm_in.soil_type,
        irrigation_source=farm_in.irrigation_source,
        total_area_acres=farm_in.total_area_acres
    )
    db.add(farm)
    db.commit()
    db.refresh(farm)
    return farm

@router.get("/crops", response_model=List[CropCatalogResponse])
def get_crop_catalog(db: Session = Depends(get_db)):
    crops = db.query(CropCatalog).all()
    results = []
    for c in crops:
        stages = [{"id": s.id, "stage_name": s.stage_name, "typical_days": s.typical_days, "susceptibility_multiplier": s.susceptibility_multiplier} for s in c.stages]
        varieties = [{"id": v.id, "variety_name": v.variety_name, "resistance_traits": v.resistance_traits} for v in c.varieties]
        results.append({
            "id": c.id,
            "name": c.name,
            "scientific_name": c.scientific_name,
            "category": c.category,
            "description": c.description,
            "stages": stages,
            "varieties": varieties
        })
    return results
