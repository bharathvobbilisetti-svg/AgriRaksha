import os
import shutil
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import CropCatalog
from app.core.config import UPLOAD_DIR
from ml.disease_detection.engine import disease_vision_pipeline
from app.schemas.schemas import DiseasePredictionResult

router = APIRouter(prefix="/disease", tags=["Crop Disease Vision & Pathology"])

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """
    Saves an uploaded plant image and returns the accessible URL
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a valid image (JPEG/PNG)")
        
    filename = f"leaf_{os.urandom(6).hex()}_{file.filename}"
    file_path = UPLOAD_DIR / filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {
        "filename": filename,
        "image_url": f"/uploads/{filename}",
        "status": "uploaded"
    }

@router.post("/predict", response_model=DiseasePredictionResult)
def predict_disease(
    crop_name: str = Form("Paddy (Rice)"),
    image_url: Optional[str] = Form(None),
    symptom_notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Executes Computer Vision plant diagnosis pipeline.
    Validates plant tissue, predicts condition, estimates severity,
    and flags uncertainty (needs_expert_validation).
    """
    # Run vision inference
    result = disease_vision_pipeline.analyze_image(
        image_path=image_url or "sample_paddy_rice_blast.jpg",
        crop_name=crop_name,
        symptom_hint=symptom_notes
    )
    return result
