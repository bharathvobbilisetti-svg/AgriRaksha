from typing import List, Dict, Any

class XAIExplainer:
    """
    Explainable AI (XAI) engine for crop risk attribution.
    Decomposes the final composite risk score into human-interpretable
    contributing factors with weighted impact and agronomic descriptions.
    """

    @staticmethod
    def generate_explanation(
        visual_score: float,
        weather_score: float,
        crop_susceptibility_score: float,
        geo_proximity_score: float,
        pest_pressure_score: float,
        weather_drivers: List[str] = None,
        nearby_cases_count: int = 6,
        nearby_radius_km: float = 5.0,
        pest_trend: str = "Increasing",
        crop_stage: str = "Flowering / Early Fruiting"
    ) -> List[Dict[str, Any]]:
        factors = []

        # 1. Visual Evidence Factor
        if visual_score >= 70:
            factors.append({
                "factor": "Visual Symptom Evidence",
                "score": round(visual_score, 1),
                "weight": 0.35,
                "impact": "High",
                "description": "Image indicates distinct target-board concentric lesions on leaf surface."
            })
        elif visual_score >= 40:
            factors.append({
                "factor": "Visual Symptom Evidence",
                "score": round(visual_score, 1),
                "weight": 0.35,
                "impact": "Medium",
                "description": "Image exhibits mild chlorotic discoloration requiring continued monitoring."
            })

        # 2. Weather Microclimate Suitability
        if weather_score >= 70:
            desc = "High humidity and recent rainfall accelerate fungal spore germination."
            if weather_drivers and len(weather_drivers) > 0:
                desc = f"{weather_drivers[0]}."
            factors.append({
                "factor": "Weather & Microclimate Suitability",
                "score": round(weather_score, 1),
                "weight": 0.25,
                "impact": "High",
                "description": desc
            })
        elif weather_score >= 40:
            factors.append({
                "factor": "Weather & Microclimate Suitability",
                "score": round(weather_score, 1),
                "weight": 0.25,
                "impact": "Medium",
                "description": "Moderate atmospheric humidity supports steady pathogen maintenance."
            })

        # 3. Crop Growth Stage Susceptibility
        if crop_susceptibility_score >= 65:
            factors.append({
                "factor": "Phenological Stage Susceptibility",
                "score": round(crop_susceptibility_score, 1),
                "weight": 0.15,
                "impact": "High",
                "description": f"Crop is at {crop_stage} stage, where dense foliage canopy reduces air circulation."
            })
        else:
            factors.append({
                "factor": "Phenological Stage Susceptibility",
                "score": round(crop_susceptibility_score, 1),
                "weight": 0.15,
                "impact": "Low",
                "description": "Current vegetative canopy has moderate disease resilience."
            })

        # 4. Geospatial Neighborhood Outbreak Proximity
        if geo_proximity_score >= 60:
            factors.append({
                "factor": "Neighborhood Outbreak Proximity",
                "score": round(geo_proximity_score, 1),
                "weight": 0.15,
                "impact": "High",
                "description": f"{nearby_cases_count} confirmed outbreak cases recorded within {nearby_radius_km} km radius."
            })
        elif geo_proximity_score >= 30:
            factors.append({
                "factor": "Neighborhood Outbreak Proximity",
                "score": round(geo_proximity_score, 1),
                "weight": 0.15,
                "impact": "Medium",
                "description": "Sporadic isolated cases reported in the surrounding mandal."
            })
        else:
            factors.append({
                "factor": "Neighborhood Outbreak Proximity",
                "score": round(geo_proximity_score, 1),
                "weight": 0.15,
                "impact": "Low",
                "description": "No active disease clusters within 10 km."
            })

        # 5. Local Pest Pressure
        if pest_pressure_score >= 60:
            factors.append({
                "factor": "Local Pest & Trap Pressure",
                "score": round(pest_pressure_score, 1),
                "weight": 0.10,
                "impact": "High",
                "description": f"Pest-trap count is {pest_trend.lower()} and exceeds economic threshold levels."
            })
        elif pest_pressure_score >= 35:
            factors.append({
                "factor": "Local Pest & Trap Pressure",
                "score": round(pest_pressure_score, 1),
                "weight": 0.10,
                "impact": "Medium",
                "description": "Pest population is at moderate baseline levels in nearby traps."
            })

        return factors

xai_explainer = XAIExplainer()
