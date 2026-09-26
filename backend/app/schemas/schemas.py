from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

# Auth & User
class UserLogin(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    role: str = "farmer"  # farmer, extension_worker, expert, official, admin
    phone: Optional[str] = None
    village: Optional[str] = None
    mandal: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = "Andhra Pradesh"
    preferred_language: Optional[str] = "en"

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    phone: Optional[str] = None
    village: Optional[str] = None
    mandal: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    preferred_language: str
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# Farm & Crops
class FarmCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    village: str
    mandal: str
    district: str
    state: str = "Andhra Pradesh"
    soil_type: str = "Red Loam"
    irrigation_source: str = "Drip Irrigation"
    total_area_acres: float = 2.5

class FarmResponse(BaseModel):
    id: int
    farmer_id: int
    name: str
    latitude: float
    longitude: float
    village: str
    mandal: str
    district: str
    state: str
    soil_type: str
    irrigation_source: str
    total_area_acres: float
    created_at: datetime

    class Config:
        from_attributes = True

class CropCatalogResponse(BaseModel):
    id: int
    name: str
    scientific_name: Optional[str]
    category: str
    description: Optional[str]
    stages: List[Dict[str, Any]] = []
    varieties: List[Dict[str, Any]] = []

    class Config:
        from_attributes = True

# Weather
class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    temperature_c: float
    relative_humidity_pct: float
    rainfall_mm: float
    leaf_wetness_hours: float
    wind_speed_kmh: float
    fungal_spore_germination_risk: float
    forecast_rain_prob_24h: float
    forecast_rain_prob_72h: float
    weather_condition: str
    icon: str

# Disease Diagnosis & Multimodal Risk
class DiseasePredictionResult(BaseModel):
    is_leaf_or_plant: bool
    plant_verification_confidence: float
    crop: str
    predicted_condition: str
    scientific_name: Optional[str] = None
    pathogen: Optional[str] = None
    confidence: float
    severity: str
    severity_percentage: float
    needs_expert_validation: bool
    is_confirmed: bool = False
    heatmap_url: Optional[str] = None
    class_probabilities: Optional[Dict[str, float]] = None
    disclaimer: str

class FactorExplanation(BaseModel):
    factor: str
    score: float
    weight: float
    impact: str  # High, Medium, Low
    description: str

class MultimodalRiskDetail(BaseModel):
    final_score: float  # 0 to 100
    risk_tier: str  # Low, Moderate, High, Very High
    visual_evidence_score: float
    weather_suitability_score: float
    crop_susceptibility_score: float
    geo_proximity_score: float
    pest_pressure_score: float
    factors_explanation: List[FactorExplanation]

class IPMDetail(BaseModel):
    condition_name: str
    cultural_control: str
    mechanical_control: str
    biological_control: str
    chemical_control_regulated: Optional[str]
    safety_precautions: str
    pre_harvest_interval_days: int
    extension_consultation_advised: bool
    official_disclaimer: str

class AdvisoryDetail(BaseModel):
    language_code: str
    title: str
    farmer_guidance_text: str
    action_bullet_points: List[str]
    urgency: str

class DiseaseCaseCreate(BaseModel):
    farm_id: int
    crop_id: int
    variety_id: Optional[int] = None
    stage_id: Optional[int] = None
    image_url: str
    symptom_notes: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class DiseaseCaseResponse(BaseModel):
    id: int
    case_number: str
    farmer_id: int
    farm_id: int
    crop_name: str
    variety_name: Optional[str] = None
    stage_name: Optional[str] = None
    image_url: str
    ai_predicted_condition: str
    ai_confidence: float
    estimated_severity: str
    severity_percentage: float
    needs_expert_validation: bool
    multimodal_risk_score: float
    risk_level: str
    status: str
    is_confirmed: bool
    confirmed_condition: Optional[str] = None
    heatmap_url: Optional[str] = None
    created_at: datetime
    risk_breakdown: Optional[MultimodalRiskDetail] = None
    ipm_recommendation: Optional[IPMDetail] = None
    advisories: List[AdvisoryDetail] = []
    farm_village: Optional[str] = None
    farm_mandal: Optional[str] = None
    farm_district: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True

# Pest Trap
class PestTrapResponse(BaseModel):
    id: int
    trap_code: str
    trap_type: str
    target_pest: str
    latitude: float
    longitude: float
    is_active: bool
    current_count: int
    previous_count: int
    population_trend: str
    risk_level: str
    economic_threshold_level: int
    last_observation_date: datetime
    farm_name: str
    village: str

    class Config:
        from_attributes = True

class PestPredictionResult(BaseModel):
    trap_id: Optional[str] = None
    pest_species: str
    pest_count: int
    population_trend: str
    risk_level: str
    economic_threshold_level: int
    exceeds_etl: bool
    confidence: float
    recommendation: str
    annotated_image_url: Optional[str] = None

# Expert Review
class ExpertReviewSubmission(BaseModel):
    case_id: int
    confirmed_condition: str
    diagnostic_agreement: str  # Confirmed, Modified, Refuted
    expert_severity: str
    advisory_notes: str
    recommend_field_visit: bool = False
    recommend_lab_test: bool = False
    lab_name: Optional[str] = None
    sample_type: Optional[str] = None

class ExpertReviewResponse(BaseModel):
    id: int
    case_id: int
    expert_name: str
    reviewed_at: datetime
    original_ai_condition: str
    confirmed_condition: str
    diagnostic_agreement: str
    expert_severity: str
    advisory_notes: str
    recommend_field_visit: bool
    recommend_lab_test: bool

    class Config:
        from_attributes = True

# Follow-Up Record
class FollowUpSubmission(BaseModel):
    case_id: int
    image_url: str
    farmer_notes: Optional[str] = None

class FollowUpResponse(BaseModel):
    id: int
    case_id: int
    follow_up_number: int
    submission_date: datetime
    image_url: str
    farmer_notes: Optional[str]
    foliage_condition: str
    difference_score_pct: float

    class Config:
        from_attributes = True

# Geospatial Hotspots
class HotspotCluster(BaseModel):
    id: str
    latitude: float
    longitude: float
    district: str
    mandal: str
    village: str
    dominant_crop: str
    dominant_condition: str
    total_cases: int
    confirmed_cases: int
    high_risk_count: int
    average_risk_score: float
    risk_tier: str  # High, Severe, Moderate
    active_traps_count: int
    max_pest_count: int

class HotspotGeoJSON(BaseModel):
    type: str = "FeatureCollection"
    features: List[Dict[str, Any]]

# Official Dashboard Statistics
class DashboardStats(BaseModel):
    total_monitored_farms: int
    active_cases: int
    confirmed_outbreaks: int
    high_risk_farms: int
    open_expert_triage: int
    laboratory_referrals: int
    crop_distribution: Dict[str, int]
    disease_distribution: Dict[str, int]
    pest_pressure_summary: Dict[str, Any]
    extension_response_rate_pct: float
    average_resolution_days: float
    forecast_next_7_days: List[Dict[str, Any]]
