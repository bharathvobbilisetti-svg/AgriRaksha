from datetime import datetime
import json
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
)
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(120), nullable=False)
    role = Column(String(50), default="farmer", index=True)  # farmer, extension_worker, expert, official, admin
    phone = Column(String(20), nullable=True)
    village = Column(String(100), nullable=True)
    mandal = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    state = Column(String(100), default="Andhra Pradesh")
    preferred_language = Column(String(10), default="en")  # en, hi, te
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    farms = relationship("Farm", back_populates="farmer", cascade="all, delete-orphan")
    disease_cases = relationship("DiseaseCase", back_populates="farmer")
    expert_reviews = relationship("ExpertReview", back_populates="expert")
    notifications = relationship("Notification", back_populates="user")


class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(150), nullable=False)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    village = Column(String(100), nullable=False, index=True)
    mandal = Column(String(100), nullable=False, index=True)
    district = Column(String(100), nullable=False, index=True)
    state = Column(String(100), default="Andhra Pradesh")
    soil_type = Column(String(80), default="Red Loam")  # Black Cotton, Red Loam, Alluvial, Clay Loam
    irrigation_source = Column(String(80), default="Drip Irrigation")  # Drip, Borewell, Canal, Rainfed
    total_area_acres = Column(Float, default=2.5)
    created_at = Column(DateTime, default=datetime.utcnow)

    farmer = relationship("User", back_populates="farms")
    crops = relationship("FarmerCrop", back_populates="farm", cascade="all, delete-orphan")
    disease_cases = relationship("DiseaseCase", back_populates="farm")
    traps = relationship("PestTrap", back_populates="farm")
    weather_records = relationship("WeatherRecord", back_populates="farm")


class CropCatalog(Base):
    __tablename__ = "crop_catalogs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)  # Tomato, Paddy (Rice), Cotton, Chilli, Wheat, Maize
    scientific_name = Column(String(150), nullable=True)
    category = Column(String(50), default="Horticulture")
    description = Column(Text, nullable=True)
    
    stages = relationship("CropStage", back_populates="crop")
    varieties = relationship("CropVariety", back_populates="crop")


class CropStage(Base):
    __tablename__ = "crop_stages"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crop_catalogs.id"), nullable=False)
    stage_name = Column(String(80), nullable=False)  # Seedling, Vegetative, Flowering, Fruiting, Maturity
    typical_days = Column(String(50), nullable=True)
    susceptibility_multiplier = Column(Float, default=1.0)  # Susceptibility weight for risk engine
    description = Column(String(255), nullable=True)

    crop = relationship("CropCatalog", back_populates="stages")


class CropVariety(Base):
    __tablename__ = "crop_varieties"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crop_catalogs.id"), nullable=False)
    variety_name = Column(String(100), nullable=False)  # e.g., Arka Rakshak, Pusa Ruby, BPT 5204 (Samba Mahsuri)
    resistance_traits = Column(String(255), default="Standard")
    maturity_days = Column(Integer, default=120)

    crop = relationship("CropCatalog", back_populates="varieties")


class FarmerCrop(Base):
    __tablename__ = "farmer_crops"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    crop_id = Column(Integer, ForeignKey("crop_catalogs.id"), nullable=False)
    variety_id = Column(Integer, ForeignKey("crop_varieties.id"), nullable=True)
    current_stage_id = Column(Integer, ForeignKey("crop_stages.id"), nullable=True)
    sowing_date = Column(DateTime, default=datetime.utcnow)
    area_allocated_acres = Column(Float, default=1.0)
    is_active = Column(Boolean, default=True)

    farm = relationship("Farm", back_populates="crops")
    crop = relationship("CropCatalog")
    variety = relationship("CropVariety")
    stage = relationship("CropStage")


class DiseaseCase(Base):
    __tablename__ = "disease_cases"

    id = Column(Integer, primary_key=True, index=True)
    case_number = Column(String(50), unique=True, index=True, nullable=False)  # e.g. AGR-2026-00102
    farmer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    crop_id = Column(Integer, ForeignKey("crop_catalogs.id"), nullable=False)
    variety_id = Column(Integer, ForeignKey("crop_varieties.id"), nullable=True)
    stage_id = Column(Integer, ForeignKey("crop_stages.id"), nullable=True)
    
    # Image & Input Details
    image_url = Column(String(255), nullable=False)
    is_leaf_or_plant = Column(Boolean, default=True)
    plant_verification_confidence = Column(Float, default=0.98)
    symptom_notes = Column(Text, nullable=True)
    
    # AI Prediction (Probabilistic, NOT definitive)
    ai_predicted_condition = Column(String(120), nullable=False)  # e.g., Early Blight, Late Blight, Leaf Mold, Healthy
    ai_confidence = Column(Float, nullable=False)  # 0.0 to 1.0
    estimated_severity = Column(String(30), default="Moderate")  # Mild, Moderate, Severe
    severity_percentage = Column(Float, default=25.0)  # Estimated foliage damage %
    needs_expert_validation = Column(Boolean, default=True)  # Low confidence or severe case trigger
    
    # Multimodal Risk Assessment
    multimodal_risk_score = Column(Float, default=50.0)  # 0 to 100
    risk_level = Column(String(30), default="Moderate")  # Low, Moderate, High, Very High
    
    # Ground-Truth & Expert Review status
    status = Column(String(50), default="ai_analyzed", index=True) 
    # reported, ai_analyzed, pending_expert, expert_verified, field_inspected, resolved
    is_confirmed = Column(Boolean, default=False)
    confirmed_condition = Column(String(120), nullable=True)
    heatmap_url = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    farmer = relationship("User", back_populates="disease_cases")
    farm = relationship("Farm", back_populates="disease_cases")
    crop = relationship("CropCatalog")
    variety = relationship("CropVariety")
    stage = relationship("CropStage")
    expert_review = relationship("ExpertReview", back_populates="disease_case", uselist=False)
    risk_breakdown = relationship("MultimodalRiskScore", back_populates="disease_case", uselist=False)
    ipm_recommendation = relationship("IPMRecommendation", back_populates="disease_case", uselist=False)
    advisories = relationship("MultilingualAdvisory", back_populates="disease_case")
    follow_ups = relationship("FollowUpRecord", back_populates="disease_case", cascade="all, delete-orphan")
    lab_referral = relationship("LaboratoryReferral", back_populates="disease_case", uselist=False)


class MultimodalRiskScore(Base):
    __tablename__ = "multimodal_risk_scores"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("disease_cases.id"), nullable=False, unique=True)
    visual_evidence_score = Column(Float, nullable=False)  # 0 - 100
    weather_suitability_score = Column(Float, nullable=False)  # 0 - 100
    crop_susceptibility_score = Column(Float, nullable=False)  # 0 - 100
    geo_proximity_score = Column(Float, nullable=False)  # 0 - 100 (Nearby outbreaks)
    pest_pressure_score = Column(Float, nullable=False)  # 0 - 100 (Trap count pressure)
    final_score = Column(Float, nullable=False)  # 0 - 100
    risk_tier = Column(String(30), nullable=False)  # Low, Moderate, High, Very High
    factors_explanation = Column(JSON, nullable=True)  # List of string explainability bullet points
    calculated_at = Column(DateTime, default=datetime.utcnow)

    disease_case = relationship("DiseaseCase", back_populates="risk_breakdown")


class PestTrap(Base):
    __tablename__ = "pest_traps"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=False)
    trap_code = Column(String(50), unique=True, index=True, nullable=False)  # TRAP-101
    trap_type = Column(String(50), default="Pheromone Trap")  # Pheromone, Yellow Sticky, Blue Sticky, Light Trap
    target_pest = Column(String(100), nullable=False)  # Fruit Fly, Fall Armyworm, Whitefly, Thrips, Stem Borer
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    installed_at = Column(DateTime, default=datetime.utcnow)

    farm = relationship("Farm", back_populates="traps")
    observations = relationship("TrapObservation", back_populates="trap", cascade="all, delete-orphan")


class TrapObservation(Base):
    __tablename__ = "trap_observations"

    id = Column(Integer, primary_key=True, index=True)
    trap_id = Column(Integer, ForeignKey("pest_traps.id"), nullable=False)
    observation_date = Column(DateTime, default=datetime.utcnow)
    image_url = Column(String(255), nullable=True)
    pest_species = Column(String(100), nullable=False)
    pest_count = Column(Integer, nullable=False)
    previous_count = Column(Integer, default=0)
    population_trend = Column(String(30), default="Stable")  # Increasing, Stable, Decreasing
    economic_threshold_level = Column(Integer, default=25)  # ETL threshold
    risk_level = Column(String(30), default="Moderate")  # Low, Moderate, High, Severe
    notes = Column(String(255), nullable=True)

    trap = relationship("PestTrap", back_populates="observations")


class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)
    temperature_c = Column(Float, nullable=False)
    relative_humidity_pct = Column(Float, nullable=False)
    rainfall_mm = Column(Float, default=0.0)
    leaf_wetness_hours = Column(Float, default=2.0)
    wind_speed_kmh = Column(Float, default=8.0)
    fungal_spore_germination_risk = Column(Float, default=45.0)  # 0 - 100
    forecast_rain_prob_24h = Column(Float, default=40.0)  # %
    forecast_rain_prob_72h = Column(Float, default=65.0)  # %

    farm = relationship("Farm", back_populates="weather_records")


class ExpertReview(Base):
    __tablename__ = "expert_reviews"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("disease_cases.id"), unique=True, nullable=False)
    expert_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reviewed_at = Column(DateTime, default=datetime.utcnow)
    original_ai_condition = Column(String(120), nullable=False)
    confirmed_condition = Column(String(120), nullable=False)
    diagnostic_agreement = Column(String(30), default="Confirmed")  # Confirmed, Modified, Refuted
    expert_severity = Column(String(30), default="Moderate")
    advisory_notes = Column(Text, nullable=False)
    recommend_field_visit = Column(Boolean, default=False)
    recommend_lab_test = Column(Boolean, default=False)
    approved_for_training_dataset = Column(Boolean, default=True)  # Ground-truth continuous learning loop

    disease_case = relationship("DiseaseCase", back_populates="expert_review")
    expert = relationship("User", back_populates="expert_reviews")


class IPMRecommendation(Base):
    __tablename__ = "ipm_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("disease_cases.id"), unique=True, nullable=False)
    condition_name = Column(String(120), nullable=False)
    
    # Tiered IPM strategy
    cultural_control = Column(Text, nullable=False)
    mechanical_control = Column(Text, nullable=False)
    biological_control = Column(Text, nullable=False)
    chemical_control_regulated = Column(Text, nullable=True)  # Never fabricated; includes CIBRC statutory guidance
    safety_precautions = Column(Text, nullable=False)
    pre_harvest_interval_days = Column(Integer, default=7)
    extension_consultation_advised = Column(Boolean, default=True)
    official_disclaimer = Column(Text, default="Use chemical products strictly according to label specifications approved by CIB&RC / Directorate of Plant Protection. Always wear protective gear.")

    disease_case = relationship("DiseaseCase", back_populates="ipm_recommendation")


class MultilingualAdvisory(Base):
    __tablename__ = "multilingual_advisories"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("disease_cases.id"), nullable=False)
    language_code = Column(String(10), nullable=False)  # en, hi, te
    title = Column(String(200), nullable=False)
    farmer_guidance_text = Column(Text, nullable=False)
    action_bullet_points = Column(JSON, nullable=False)
    urgency = Column(String(30), default="Normal")  # Routine, Urgent, Immediate Action

    disease_case = relationship("DiseaseCase", back_populates="advisories")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    alert_type = Column(String(50), default="risk_alert")  # disease_risk, pest_surge, outbreak_warning, expert_feedback, follow_up
    severity = Column(String(20), default="medium")  # low, medium, high, critical
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")


class FollowUpRecord(Base):
    __tablename__ = "follow_up_records"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("disease_cases.id"), nullable=False)
    follow_up_number = Column(Integer, default=1)
    submission_date = Column(DateTime, default=datetime.utcnow)
    image_url = Column(String(255), nullable=False)
    farmer_notes = Column(Text, nullable=True)
    foliage_condition = Column(String(50), default="Improving")  # Improving, Stable, Deteriorating, Fully Recovered
    difference_score_pct = Column(Float, default=-30.0)  # -30% lesion area reduction

    disease_case = relationship("DiseaseCase", back_populates="follow_ups")


class LaboratoryReferral(Base):
    __tablename__ = "laboratory_referrals"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("disease_cases.id"), unique=True, nullable=False)
    lab_name = Column(String(150), default="Regional Krishi Vigyan Kendra (KVK) Plant Health Lab")
    sample_type = Column(String(50), default="Leaf Tissue")  # Leaf Tissue, Stem Cutting, Soil Sample
    referral_reason = Column(String(255), nullable=False)
    status = Column(String(50), default="Sample Dispatched")  # Sample Dispatched, In Analysis, Completed
    findings = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    disease_case = relationship("DiseaseCase", back_populates="lab_referral")
