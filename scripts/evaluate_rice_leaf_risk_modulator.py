# -*- coding: utf-8 -*-
"""
AgriRaksha - Rice Leaf AUG Multimodal Risk Modulator Pipeline Evaluator.
Executes the end-to-end crop intelligence flow:
Image -> DL MobileNetV2 Vision -> Lesion Damage % -> Multimodal Risk Modulator -> XAI -> IPM
"""

import os
import sys
import json
import time
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "backend"))

from ml.disease_detection.engine import disease_vision_pipeline
from backend.app.services.multimodal_risk import multimodal_risk_service
from backend.app.services.ipm_service import ipm_service
from backend.app.services.advisory_service import advisory_service

DATA_DIR = BASE_DIR / "Rice_Leaf_AUG"
OUTPUT_FILE = BASE_DIR / "data" / "rice_leaf_risk_modulation_results.json"
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("AGRIRAKSHA - RICE LEAF AUG MULTIMODAL RISK MODULATION ENGINE")
print("=" * 80)

class_dirs = sorted([d for d in DATA_DIR.iterdir() if d.is_dir()])
results = []

for d in class_dirs:
    imgs = list(d.glob("*.jpg")) + list(d.glob("*.png")) + list(d.glob("*.jpeg"))
    if not imgs:
        continue
    
    test_img = imgs[0]
    category_name = d.name
    
    print(f"\n--- Processing: {category_name} ({test_img.name}) ---")
    
    # 1. Computer Vision & Lesion Segmentation Pipeline
    t0 = time.time()
    vision_res = disease_vision_pipeline.analyze_image(
        image_path=str(test_img),
        crop_name="Paddy (Rice)"
    )
    cv_time = time.time() - t0
    
    predicted_cond = vision_res["predicted_condition"]
    confidence = vision_res["confidence"]
    severity = vision_res["severity"]
    sev_pct = vision_res["severity_percentage"]
    heatmap_url = vision_res.get("heatmap_url")
    
    # 2. Agro-Weather Microclimate Context
    is_healthy = "healthy" in predicted_cond.lower()
    weather_score = 35.0 if is_healthy else 84.0
    weather_drivers = [
        "Relative humidity at 86% with persistent morning dew fosters blast & blight propagation."
    ] if not is_healthy else [
        "Optimal sunshine and ambient humidity maintain healthy canopy respiration."
    ]
    
    # 3. Spatio-temporal Outbreak Proximity & Pest Trap Context
    nearby_cases = 0 if is_healthy else 6
    pest_count = 14 if is_healthy else 38
    stage_multiplier = 1.0 if is_healthy else 1.35
    stage_name = "Tillering to Panicle Initiation"
    
    # 4. Multimodal Risk Modulator
    t1 = time.time()
    risk_res = multimodal_risk_service.calculate_risk(
        ai_confidence=confidence,
        condition_name=predicted_cond,
        weather_score=weather_score,
        crop_stage_multiplier=stage_multiplier,
        nearby_confirmed_cases=nearby_cases,
        nearby_radius_km=5.0,
        pest_trap_count=pest_count,
        pest_etl=20,
        weather_drivers=weather_drivers,
        crop_stage_name=stage_name
    )
    risk_time = time.time() - t1
    
    # 5. Integrated Pest Management (IPM) & Vernacular Advisories
    ipm = ipm_service.get_recommendation(predicted_cond)
    advisories = advisory_service.generate_advisories(predicted_cond)
    
    summary_item = {
        "true_dataset_category": category_name,
        "sample_image": str(test_img.name),
        "vision_ai": {
            "predicted_condition": predicted_cond,
            "scientific_name": vision_res.get("scientific_name"),
            "confidence_pct": round(confidence * 100, 1),
            "severity_level": severity,
            "damage_percentage": sev_pct,
            "heatmap_url": heatmap_url,
            "needs_expert_validation": vision_res.get("needs_expert_validation")
        },
        "risk_modulator": {
            "final_composite_score": risk_res["final_score"],
            "risk_tier": risk_res["risk_tier"],
            "visual_evidence_score": risk_res["visual_evidence_score"],
            "weather_suitability_score": risk_res["weather_suitability_score"],
            "crop_susceptibility_score": risk_res["crop_susceptibility_score"],
            "geo_proximity_score": risk_res["geo_proximity_score"],
            "pest_pressure_score": risk_res["pest_pressure_score"],
            "top_xai_factors": risk_res["factors_explanation"][:3]
        },
        "ipm_cultural_control": ipm.get("cultural_control", "")[:120] + "...",
        "ipm_chemical_cibrc": ipm.get("chemical_control_regulated", "")[:120] + "...",
        "telugu_advisory": next((a["title"] for a in advisories if a["language_code"] == "te"), "")
    }
    results.append(summary_item)
    
    print(f"  • Predicted Disease : {predicted_cond} ({confidence*100:.1f}%)")
    print(f"  • Foliage Damage    : {sev_pct}% ({severity})")
    print(f"  • Risk Modulator    : {risk_res['final_score']} / 100 [{risk_res['risk_tier'].upper()} RISK]")
    print(f"  • Visual: {risk_res['visual_evidence_score']} | Weather: {risk_res['weather_suitability_score']} | Stage: {risk_res['crop_susceptibility_score']} | Geo: {risk_res['geo_proximity_score']} | Trap: {risk_res['pest_pressure_score']}")
    print(f"  • Heatmap Saved     : {heatmap_url}")

# Save JSON results
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\n" + "=" * 80)
print(f"EVALUATION COMPLETED: All {len(results)} Rice Leaf AUG classes modulated.")
print(f"Results saved to: {OUTPUT_FILE}")
print("=" * 80)
