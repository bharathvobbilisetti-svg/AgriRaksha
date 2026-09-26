import math
from typing import Dict, Any, List, Optional
from app.core.config import settings
from ml.xai.explainer import xai_explainer

class MultimodalRiskEngine:
    """
    Multimodal Risk Fusion Service.
    Combines:
    1. AI Visual Pathology Evidence (w1 = 0.35)
    2. Agro-Weather Microclimate Suitability (w2 = 0.25)
    3. Crop Phenological Susceptibility (w3 = 0.15)
    4. Spatio-Temporal Outbreak Kernel (w4 = 0.15)
    5. Pest Surveillance Pressure (w5 = 0.10)
    
    Produces normalized 0-100 score + Explainable Factor Breakdown (XAI).
    """

    @staticmethod
    def calculate_spatio_temporal_outbreak_score(
        nearby_confirmed_cases: int,
        nearby_radius_km: float = 5.0,
        average_case_distance_km: Optional[float] = None,
        sigma_distance_km: float = 4.5,
        average_days_elapsed: float = 4.0,
        tau_days: float = 14.0
    ) -> float:
        """
        Calculates geospatial epidemic pressure using Gaussian spatial distance
        and exponential temporal decay kernels:
        K(d, t) = sum( exp(-d_i^2 / (2 * sigma^2)) * exp(-delta_t / tau) )
        """
        if nearby_confirmed_cases <= 0:
            return 0.0

        d = average_case_distance_km if average_case_distance_km is not None else (nearby_radius_km * 0.55)
        # Spatial Gaussian decay
        spatial_kernel = math.exp(-(d ** 2) / (2.0 * (sigma_distance_km ** 2)))
        # Temporal exponential decay
        temporal_kernel = math.exp(-average_days_elapsed / tau_days)
        
        # Cumulative epidemiological pressure
        effective_case_mass = nearby_confirmed_cases * spatial_kernel * temporal_kernel
        
        # Sigmoid saturation to 0 - 100
        # 1-2 cases -> 25-45 (Moderate), 5-7 cases -> 65-80 (High), 10+ cases -> 90+ (Very High)
        score = 100.0 * (1.0 - math.exp(-effective_case_mass / 3.2))
        return round(min(100.0, max(0.0, score)), 1)

    def calculate_risk(
        self,
        ai_confidence: float,
        condition_name: str,
        weather_score: float,
        crop_stage_multiplier: float = 1.2,
        nearby_confirmed_cases: int = 6,
        nearby_radius_km: float = 5.0,
        pest_trap_count: int = 37,
        pest_etl: int = 20,
        weather_drivers: List[str] = None,
        crop_stage_name: str = "Fruiting / Maturation",
        average_case_distance_km: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Executes mathematically principled multimodal risk fusion.
        Zero hardcoded score overrides.
        """
        # 1. Visual Score (0 - 100)
        if condition_name.lower().startswith("healthy"):
            visual_score = max(0.0, (1.0 - ai_confidence) * 15.0)
        else:
            visual_score = min(100.0, max(10.0, ai_confidence * 100.0))

        # 2. Agro-Weather Score (0 - 100)
        w_score = min(100.0, max(0.0, weather_score))

        # 3. Crop Stage Susceptibility Score (0 - 100)
        # Multiplier typically ranges 0.8 (seedling) to 1.4 (dense flowering/fruiting canopy)
        stage_score = min(100.0, max(10.0, crop_stage_multiplier * 55.0))

        # 4. Spatio-Temporal Geospatial Outbreak Pressure (0 - 100)
        geo_score = self.calculate_spatio_temporal_outbreak_score(
            nearby_confirmed_cases=nearby_confirmed_cases,
            nearby_radius_km=nearby_radius_km,
            average_case_distance_km=average_case_distance_km
        )

        # 5. Pest Surveillance Pressure (0 - 100)
        etl_ratio = pest_trap_count / float(max(1, pest_etl))
        pest_score = min(100.0, max(0.0, (etl_ratio ** 0.85) * 45.0))

        # Weighted composite score using calibrated domain weights
        composite_score = (
            (visual_score * settings.WEIGHT_VISUAL) +
            (w_score * settings.WEIGHT_WEATHER) +
            (stage_score * settings.WEIGHT_CROP_STAGE) +
            (geo_score * settings.WEIGHT_GEO_HISTORY) +
            (pest_score * settings.WEIGHT_PEST_PRESSURE)
        )

        final_score = round(min(100.0, max(0.0, composite_score)), 1)

        # Scientific Risk Tiers
        if final_score >= 81.0:
            risk_tier = "Very High"
        elif final_score >= 51.0:
            risk_tier = "High"
        elif final_score >= 26.0:
            risk_tier = "Moderate"
        else:
            risk_tier = "Low"

        # Generate Explainable AI factor attribution
        factors = xai_explainer.generate_explanation(
            visual_score=visual_score,
            weather_score=w_score,
            crop_susceptibility_score=stage_score,
            geo_proximity_score=geo_score,
            pest_pressure_score=pest_score,
            weather_drivers=weather_drivers,
            nearby_cases_count=nearby_confirmed_cases,
            nearby_radius_km=nearby_radius_km,
            pest_trend="Increasing" if pest_trap_count > pest_etl else "Stable",
            crop_stage=crop_stage_name
        )

        return {
            "final_score": final_score,
            "risk_tier": risk_tier,
            "visual_evidence_score": round(visual_score, 1),
            "weather_suitability_score": round(w_score, 1),
            "crop_susceptibility_score": round(stage_score, 1),
            "geo_proximity_score": round(geo_score, 1),
            "pest_pressure_score": round(pest_score, 1),
            "factors_explanation": factors
        }

multimodal_risk_service = MultimodalRiskEngine()
