from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import DiseaseCase, ExpertReview, LaboratoryReferral, Notification, User
from app.schemas.schemas import ExpertReviewSubmission, ExpertReviewResponse
from ml.training.trainer import crop_trainer

router = APIRouter(prefix="/expert", tags=["Expert Validation & Continuous Learning"])

@router.get("/queue")
def get_triage_queue(db: Session = Depends(get_db)):
    """
    Returns pending cases requiring expert validation (low confidence, severe condition, or farmer request).
    """
    cases = db.query(DiseaseCase).filter(
        DiseaseCase.status.in_(["pending_expert", "ai_analyzed"]),
        DiseaseCase.is_confirmed == False
    ).order_by(DiseaseCase.multimodal_risk_score.desc()).all()

    results = []
    for c in cases:
        results.append({
            "case_id": c.id,
            "case_number": c.case_number,
            "farmer_name": c.farmer.full_name if c.farmer else "Farmer",
            "village": c.farm.village if c.farm else "Unknown",
            "crop": c.crop.name if c.crop else "Tomato",
            "image_url": c.image_url,
            "ai_predicted_condition": c.ai_predicted_condition,
            "ai_confidence": round(c.ai_confidence * 100, 1),
            "severity": c.estimated_severity,
            "severity_percentage": c.severity_percentage,
            "risk_score": c.multimodal_risk_score,
            "symptom_notes": c.symptom_notes,
            "heatmap_url": getattr(c, "heatmap_url", None),
            "created_at": c.created_at
        })
    return results

@router.post("/review", response_model=ExpertReviewResponse)
def submit_expert_review(review_in: ExpertReviewSubmission, expert_id: int = 2, db: Session = Depends(get_db)):
    """
    Submits agronomist diagnostic confirmation, sets severity, writes localized advice,
    triggers laboratory referral if necessary, and marks sample as ground-truth for continuous ML learning.
    """
    case = db.query(DiseaseCase).filter(DiseaseCase.id == review_in.case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    expert = db.query(User).filter(User.id == expert_id).first()
    expert_name = expert.full_name if expert else "Expert Agronomist"

    # Update or create review
    existing_review = db.query(ExpertReview).filter(ExpertReview.case_id == case.id).first()
    if existing_review:
        existing_review.confirmed_condition = review_in.confirmed_condition
        existing_review.diagnostic_agreement = review_in.diagnostic_agreement
        existing_review.expert_severity = review_in.expert_severity
        existing_review.advisory_notes = review_in.advisory_notes
        existing_review.recommend_field_visit = review_in.recommend_field_visit
        existing_review.recommend_lab_test = review_in.recommend_lab_test
        review_obj = existing_review
    else:
        review_obj = ExpertReview(
            case_id=case.id,
            expert_id=expert_id,
            reviewed_at=datetime.utcnow(),
            original_ai_condition=case.ai_predicted_condition,
            confirmed_condition=review_in.confirmed_condition,
            diagnostic_agreement=review_in.diagnostic_agreement,
            expert_severity=review_in.expert_severity,
            advisory_notes=review_in.advisory_notes,
            recommend_field_visit=review_in.recommend_field_visit,
            recommend_lab_test=review_in.recommend_lab_test,
            approved_for_training_dataset=True
        )
        db.add(review_obj)

    # Update the case state to confirmed
    case.is_confirmed = True
    case.confirmed_condition = review_in.confirmed_condition
    case.estimated_severity = review_in.expert_severity
    case.status = "expert_verified"

    # Handle lab referral if requested
    if review_in.recommend_lab_test:
        lab_ref = LaboratoryReferral(
            case_id=case.id,
            lab_name=review_in.lab_name or "Regional KVK Plant Pathology Laboratory",
            sample_type=review_in.sample_type or "Leaf Tissue",
            referral_reason=f"Expert confirmed {review_in.confirmed_condition}. Requested pathogen culture & resistance assay.",
            status="Sample Dispatched"
        )
        db.add(lab_ref)

    # Send Notification to Farmer
    db.add(Notification(
        user_id=case.farmer_id,
        title=f"Expert Validated: {review_in.confirmed_condition}",
        message=f"{expert_name} has verified your diagnosis. Advice: {review_in.advisory_notes[:120]}...",
        alert_type="expert_feedback",
        severity="medium"
    ))

    # Ingest into active continuous learning loop
    crop_trainer.record_expert_verified_sample(
        case_id=case.id,
        image_url=case.image_url,
        predicted_condition=case.ai_predicted_condition,
        confirmed_condition=review_in.confirmed_condition,
        crop_name=case.crop.name if case.crop else "Crop",
        expert_name=expert_name,
        severity=review_in.expert_severity
    )

    db.commit()
    db.refresh(review_obj)

    return {
        "id": review_obj.id,
        "case_id": case.id,
        "expert_name": expert_name,
        "reviewed_at": review_obj.reviewed_at,
        "original_ai_condition": review_obj.original_ai_condition,
        "confirmed_condition": review_obj.confirmed_condition,
        "diagnostic_agreement": review_obj.diagnostic_agreement,
        "expert_severity": review_obj.expert_severity,
        "advisory_notes": review_obj.advisory_notes,
        "recommend_field_visit": review_obj.recommend_field_visit,
        "recommend_lab_test": review_obj.recommend_lab_test
    }

@router.get("/training-stats")
def get_continuous_learning_stats():
    """
    Returns statistics on the continuous learning dataset and verified sample distributions.
    """
    return crop_trainer.get_dataset_summary()

@router.post("/retrain")
def trigger_continuous_retraining(epochs: int = 10, batch_size: int = 16):
    """
    Triggers incremental model transfer learning incorporating newly expert-verified ground truth.
    """
    return crop_trainer.run_training_cycle(epochs=epochs, batch_size=batch_size)
