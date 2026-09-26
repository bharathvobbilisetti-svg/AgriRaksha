# Testing & Quality Assurance Suite — AgriRaksha (SIH 2026)

This document outlines the testing strategy, automated test commands, and quality benchmarks for AgriRaksha.

---

## 🧪 1. Backend Automated Tests (PyTest)

AgriRaksha includes an automated test suite in `backend/tests/test_api.py` covering 14 critical scenarios.

### Running PyTest:
```bash
python -m pytest backend/tests/ -v
```

### Verified Test Cases:
| Test ID | Test Function | Verified Behavior | Status |
| :--- | :--- | :--- | :--- |
| **TC-01** | `test_health_check` | Validates FastAPI engine health and API version. | **PASSED** |
| **TC-02** | `test_auth_login` | Validates JWT token generation and role persistence. | **PASSED** |
| **TC-03** | `test_switch_role` | Validates instant demo role switching for pitch. | **PASSED** |
| **TC-04** | `test_get_crop_catalog` | Validates commercial crops, stages, and multipliers. | **PASSED** |
| **TC-05** | `test_weather_endpoint` | Validates microclimate humidity and spore risk. | **PASSED** |
| **TC-06** | `test_disease_prediction` | Validates CV pipeline, 87% confidence, uncertainty. | **PASSED** |
| **TC-07** | `test_pest_prediction` | Validates trap count 37, increasing trend, ETL breach. | **PASSED** |
| **TC-08** | `test_multimodal_risk_calculation` | Validates 78/100 HIGH composite score & XAI factors. | **PASSED** |
| **TC-09** | `test_gis_hotspots_geojson` | Validates GeoJSON format and feature collections. | **PASSED** |
| **TC-10** | `test_expert_review_submission` | Validates pathologist confirmation & field visit dispatch. | **PASSED** |
| **TC-11** | `test_ipm_recommendations` | Validates non-chemical priority & CIB&RC disclaimers. | **PASSED** |
| **TC-12** | `test_multilingual_advisories` | Validates translations in EN, HI, and TE. | **PASSED** |
| **TC-13** | `test_dashboard_statistics` | Validates 105 farms, 6 confirmed outbreaks, 7-day curve. | **PASSED** |
| **TC-14** | `test_ml_evaluation_metrics` | Validates scikit-learn accuracy, precision, recall, F1. | **PASSED** |

---

## 🎬 2. End-to-End Demonstration Verification

Run the end-to-end demonstration script to verify all 10 workflow phases programmatically:
```bash
python scripts/run_demo_scenario.py
```
This tests:
1. One-click demo seeder (105 farms, 25 traps).
2. Farmer symptom upload (Tomato Early Blight).
3. Vision inference (87% confidence, Moderate severity).
4. Microclimate weather risk (86% humidity, 18.5mm rain).
5. Pest trap surveillance (`TRAP-102` count 37, ETL breach).
6. Geospatial outbreak check (6 confirmed cases in 5 km).
7. Multimodal risk fusion (78/100 HIGH) and XAI attribution.
8. Tiered IPM guidance and statutory disclaimers.
9. Multilingual advisories in English, Hindi, and Telugu.
10. Expert validation and continuous learning dataset inclusion.
11. Longitudinal Day 7 follow-up showing 35% lesion reduction.
12. Scikit-Learn evaluation pipeline with confusion matrix.

---

## 💻 3. Frontend Build & Type Validation

Run TypeScript type check and production bundling:
```bash
cd frontend
npm run build
```
*Result:*
`✓ built in 2.12s` with 0 TypeScript compilation or linting errors.

---

## 🛡️ 4. Error Handling Verification

The system includes resilient error handling for agricultural edge cases:
* **Non-Plant Foliage**: Plant validation rejects non-plant images (e.g. soil, household items) with informative feedback.
* **Missing Weather Readings**: Falls back to regional Automatic Weather Station (AWS) baseline profiles.
* **Low AI Confidence**: Diagnoses with confidence $< 0.75$ automatically flag `needs_expert_validation = True` and route to the agronomist review queue.
* **Chemical Safety Enforcement**: If chemical treatments are queried without agronomist review, the system refuses unauthorized dosage prescription and mandates extension officer consultation.
