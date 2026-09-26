# Database Architecture & Relational Schema — AgriRaksha (SIH 2026)

## 1. Relational Architecture & Dual Mode

AgriRaksha implements an adaptive database layer built on **SQLAlchemy 2.0 ORM**:
1. **Local & Demo Execution (Default)**: Runs on **SQLite** with high-precision spherical Haversine trigonometric indexing. Requires zero external database server setup, enabling instant plug-and-play evaluation during hackathon judging.
2. **Production Enterprise Mode**: Drop-in compatible with **PostgreSQL + PostGIS** by configuring the `DATABASE_URL` environment variable:
   ```bash
   DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/agriraksha
   ```

---

## 2. Entity Relationship Overview

```mermaid
erDiagram
    USERS ||--o{ FARMS : owns
    USERS ||--o{ DISEASE_CASES : reports
    USERS ||--o{ EXPERT_REVIEWS : conducts
    USERS ||--o{ NOTIFICATIONS : receives

    FARMS ||--o{ FARMER_CROPS : cultivates
    FARMS ||--o{ PEST_TRAPS : hosts
    FARMS ||--o{ WEATHER_RECORDS : monitors
    FARMS ||--o{ DISEASE_CASES : locates

    CROP_CATALOGS ||--o{ CROP_STAGES : defines
    CROP_CATALOGS ||--o{ CROP_VARIETIES : defines
    CROP_CATALOGS ||--o{ FARMER_CROPS : categorizes

    PEST_TRAPS ||--o{ TRAP_OBSERVATIONS : records

    DISEASE_CASES ||--|| MULTIMODAL_RISK_SCORES : calculates
    DISEASE_CASES ||--|| EXPERT_REVIEWS : verified_by
    DISEASE_CASES ||--|| IPM_RECOMMENDATIONS : prescribes
    DISEASE_CASES ||--o{ MULTILINGUAL_ADVISORIES : generates
    DISEASE_CASES ||--o{ FOLLOW_UP_RECORDS : tracks
    DISEASE_CASES ||--o{ LABORATORY_REFERRALS : refers
```

---

## 3. Core Database Tables & Data Dictionary

### `users`
* `id` (PK, Integer)
* `email` (Unique, String)
* `hashed_password` (String, PBKDF2-HMAC-SHA256)
* `full_name` (String)
* `role` (Enum: `farmer`, `extension_worker`, `expert`, `official`, `admin`)
* `village`, `mandal`, `district`, `state` (Strings)
* `preferred_language` (`en`, `hi`, `te`)

### `farms`
* `id` (PK, Integer)
* `farmer_id` (FK -> `users.id`)
* `name` (String)
* `latitude`, `longitude` (Float, Indexed for spatial proximity)
* `village`, `mandal`, `district`, `state` (Strings, Indexed)
* `soil_type` (`Red Loam`, `Black Cotton`, `Alluvial`, `Clay Loam`)
* `irrigation_source` (`Drip`, `Borewell`, `Canal`, `Rainfed`)
* `total_area_acres` (Float)

### `crop_catalogs`, `crop_stages`, `crop_varieties`
* Defines commercial crops (Tomato, Paddy, Cotton, Chilli), stages (Seedling, Vegetative, Flowering, Fruiting), and susceptibility multipliers ($0.7 \times$ to $1.4 \times$).

### `disease_cases`
* `id` (PK, Integer)
* `case_number` (Unique, String, e.g. `AGR-2026-TOM-01`)
* `farmer_id`, `farm_id`, `crop_id`, `stage_id` (FKs)
* `image_url` (String)
* `is_leaf_or_plant` (Boolean)
* `ai_predicted_condition` (String, e.g. `Early Blight`)
* `ai_confidence` (Float, $0.0 - 1.0$)
* `estimated_severity` (`Mild`, `Moderate`, `Severe`)
* `severity_percentage` (Float, e.g. $28.5\%$)
* `needs_expert_validation` (Boolean)
* `multimodal_risk_score` (Float, $0 - 100$)
* `risk_level` (`Low`, `Moderate`, `High`, `Very High`)
* `status` (`reported`, `ai_analyzed`, `pending_expert`, `expert_verified`, `resolved`)
* `is_confirmed` (Boolean, `False` until human expert verification)
* `confirmed_condition` (String)

### `pest_traps` & `trap_observations`
* Stores trap hardware codes, target pests (Fruit Fly, Fall Armyworm), daily specimen counts, velocity trends (`Increasing`, `Stable`, `Decreasing`), and ETL breach flags.

### `expert_reviews`
* Captures ground-truth verification: pathologist ID, agreement flag (`Confirmed`, `Modified`, `Refuted`), expert severity, clinical notes, field visit orders, and `approved_for_training_dataset` continuous learning flag.

### `ipm_recommendations` & `multilingual_advisories`
* Stores tiered cultural, mechanical, biological, and cautious chemical controls with statutory safety disclaimers, plus localized strings in English, Hindi, and Telugu.
