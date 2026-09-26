# REST API Specification — AgriRaksha (SIH 2026)

All endpoints conform to standard REST conventions and are documented interactively via OpenAPI / Swagger at:  
**`http://127.0.0.1:8000/docs`**

---

## 1. Authentication & RBAC

### `POST /api/auth/login`
Authenticates a user and returns a signed bearer token.
* **Request Body:**
  ```json
  {
    "email": "farmer@agriraksha.in",
    "password": "farmer123"
  }
  ```
* **Response (200 OK):**
  ```json
  {
    "access_token": "<token>",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "email": "farmer@agriraksha.in",
      "full_name": "Ramesh Reddy",
      "role": "farmer",
      "village": "Geesugonda",
      "district": "Warangal"
    }
  }
  ```

### `POST /api/auth/switch-role/{role_name}`
Hackathon demonstration utility to immediately switch roles (`farmer`, `expert`, `official`, `extension_worker`).

---

## 2. Crop Disease Vision & Pathology

### `POST /api/disease/predict`
Executes plant tissue verification and computer vision symptom classification.
* **Form Parameters:**
  - `crop_name`: "Tomato"
  - `image_url`: "sample_tomato_early_blight.jpg"
  - `symptom_notes`: "Concentric rings on lower leaves"
* **Response (200 OK):**
  ```json
  {
    "is_leaf_or_plant": true,
    "plant_verification_confidence": 0.95,
    "crop": "Tomato",
    "predicted_condition": "Early Blight",
    "confidence": 0.87,
    "severity": "Moderate",
    "severity_percentage": 28.5,
    "needs_expert_validation": true,
    "is_confirmed": false,
    "disclaimer": "AI prediction is probabilistic and based on visual symptom patterns. It must not be considered a confirmed laboratory diagnosis until verified by an agricultural expert."
  }
  ```

---

## 3. Pest Trap Surveillance

### `POST /api/pest/predict`
Simulates smart pheromone/sticky trap image counting and population velocity analysis.
* **Form Parameters:**
  - `trap_id`: "TRAP-102"
  - `target_pest`: "Fruit Fly"
  - `current_count`: 37
  - `previous_count`: 18
* **Response (200 OK):**
  ```json
  {
    "trap_id": "TRAP-102",
    "pest_species": "Bactrocera dorsalis",
    "pest_count": 37,
    "population_trend": "Increasing",
    "risk_level": "High",
    "economic_threshold_level": 20,
    "exceeds_etl": true,
    "confidence": 0.93,
    "recommendation": "Exceeds ETL. Replenish lure, install 6-8 traps per acre, collect fallen fruits."
  }
  ```

---

## 4. Multimodal Risk Fusion & Explainable AI (XAI)

### `POST /api/risk/calculate`
Synthesizes visual symptoms, weather microclimate, growth stage, neighborhood proximity, and trap pressure.
* **Form Parameters:**
  - `crop_name`: "Tomato"
  - `condition_name`: "Early Blight"
  - `ai_confidence`: 0.87
  - `latitude`: 17.9782
  - `longitude`: 79.6251
  - `crop_stage_multiplier`: 1.4
* **Response (200 OK):**
  ```json
  {
    "final_score": 78.0,
    "risk_tier": "High",
    "visual_evidence_score": 87.0,
    "weather_suitability_score": 82.0,
    "crop_susceptibility_score": 77.0,
    "geo_proximity_score": 87.0,
    "pest_pressure_score": 77.7,
    "factors_explanation": [
      {
        "factor": "Visual Symptom Evidence",
        "score": 87.0,
        "weight": 0.35,
        "impact": "High",
        "description": "Image indicates distinct target-board concentric lesions on leaf surface."
      },
      {
        "factor": "Weather & Microclimate Suitability",
        "score": 82.0,
        "weight": 0.25,
        "impact": "High",
        "description": "High relative humidity (86%) and recent rainfall (18.5 mm) accelerate spore germination."
      },
      {
        "factor": "Neighborhood Outbreak Proximity",
        "score": 87.0,
        "weight": 0.15,
        "impact": "High",
        "description": "6 confirmed outbreak cases recorded within 5.0 km radius."
      }
    ]
  }
  ```

---

## 5. Geospatial Hotspots & GIS

### `GET /api/hotspots/geojson`
Returns standard GeoJSON FeatureCollection of all farms, active disease cases, and smart traps for Leaflet rendering.

### `GET /api/hotspots/clusters`
Returns ranked village-level disease clusters with confirmed case counts and average risk scores.

---

## 6. Expert Review & Continuous Learning

### `POST /api/expert/review`
Submits agronomist diagnostic confirmation, dispatches field inspection, and approves specimen for ML retraining.
* **Request Body:**
  ```json
  {
    "case_id": 1,
    "confirmed_condition": "Early Blight",
    "diagnostic_agreement": "Confirmed",
    "expert_severity": "Moderate",
    "advisory_notes": "Early Blight confirmed by KVK Pathology wing. Recommended immediate canopy sanitation and bio-fungicide protective spray.",
    "recommend_field_visit": true,
    "recommend_lab_test": false
  }
  ```

---

## 7. Integrated Pest Management & Advisories

### `GET /api/ipm/recommendations?condition=Early+Blight`
Returns tiered cultural, mechanical, biological, and statutory chemical guidance with safety precautions and CIB&RC disclaimer.

### `GET /api/advisories?condition=Early+Blight`
Returns localized farmer-friendly advisory texts in English (`en`), Hindi (`hi`), and Telugu (`te`).

---

## 8. Agriculture Official Dashboard

### `GET /api/dashboard/statistics`
Returns district surveillance metrics: monitored farms, confirmed outbreaks, crop-wise case distributions, trap pressure summaries, and 7-day epidemic risk trajectory forecasts.
