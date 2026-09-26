import math
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.db.models import Farm, DiseaseCase, PestTrap, TrapObservation

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Computes great-circle distance between two coordinates in kilometers.
    """
    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2.0) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c

class GISService:
    """
    Geospatial Hotspot & Surveillance Analytics Service.
    Computes spatial proximity, disease cluster densities, buffer zones,
    and GeoJSON data for Leaflet frontend maps.
    """

    @staticmethod
    def get_nearby_confirmed_cases(
        db: Session,
        lat: float,
        lon: float,
        radius_km: float = 5.0,
        condition: str = None
    ) -> List[DiseaseCase]:
        cases = db.query(DiseaseCase).join(Farm).all()
        nearby = []
        for c in cases:
            # Check if case is confirmed or severe
            if c.is_confirmed or c.multimodal_risk_score >= 65:
                if condition and c.ai_predicted_condition != condition:
                    continue
                dist = haversine_distance_km(lat, lon, c.farm.latitude, c.farm.longitude)
                if dist <= radius_km:
                    nearby.append(c)
        return nearby

    @staticmethod
    def generate_hotspots_geojson(db: Session) -> Dict[str, Any]:
        """
        Generates GeoJSON FeatureCollection of all active cases, traps, and clusters.
        """
        features = []
        cases = db.query(DiseaseCase).join(Farm).all()

        for c in cases:
            risk_color = "#10B981"  # green
            if c.multimodal_risk_score >= 76:
                risk_color = "#EF4444"  # red
            elif c.multimodal_risk_score >= 51:
                risk_color = "#F59E0B"  # amber
            elif c.multimodal_risk_score >= 26:
                risk_color = "#3B82F6"  # blue

            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [c.farm.longitude, c.farm.latitude]
                },
                "properties": {
                    "type": "disease_case",
                    "case_id": c.id,
                    "case_number": c.case_number,
                    "crop": c.crop.name if c.crop else "Unknown",
                    "condition": c.confirmed_condition or c.ai_predicted_condition,
                    "is_confirmed": c.is_confirmed,
                    "confidence": round(c.ai_confidence * 100, 1),
                    "severity": c.estimated_severity,
                    "risk_score": c.multimodal_risk_score,
                    "risk_level": c.risk_level,
                    "status": c.status,
                    "village": c.farm.village,
                    "mandal": c.farm.mandal,
                    "district": c.farm.district,
                    "marker_color": risk_color
                }
            })

        # Add Pest Traps
        traps = db.query(PestTrap).join(Farm).all()
        for t in traps:
            latest_obs = db.query(TrapObservation).filter(TrapObservation.trap_id == t.id).order_by(TrapObservation.observation_date.desc()).first()
            count = latest_obs.pest_count if latest_obs else 0
            trend = latest_obs.population_trend if latest_obs else "Stable"
            risk = latest_obs.risk_level if latest_obs else "Low"

            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [t.longitude, t.latitude]
                },
                "properties": {
                    "type": "pest_trap",
                    "trap_id": t.id,
                    "trap_code": t.trap_code,
                    "trap_type": t.trap_type,
                    "target_pest": t.target_pest,
                    "current_count": count,
                    "trend": trend,
                    "risk_level": risk,
                    "village": t.farm.village,
                    "mandal": t.farm.mandal,
                    "marker_color": "#8B5CF6"  # purple
                }
            })

        return {
            "type": "FeatureCollection",
            "features": features
        }

    @staticmethod
    def get_village_clusters(db: Session) -> List[Dict[str, Any]]:
        """
        Aggregates cases by village for hotspot ranking.
        """
        farms = db.query(Farm).all()
        village_map = {}

        for f in farms:
            v_key = f"{f.village}, {f.mandal}"
            if v_key not in village_map:
                village_map[v_key] = {
                    "village": f.village,
                    "mandal": f.mandal,
                    "district": f.district,
                    "lat": f.latitude,
                    "lon": f.longitude,
                    "cases": [],
                    "traps": []
                }
            village_map[v_key]["cases"].extend(f.disease_cases)
            village_map[v_key]["traps"].extend(f.traps)

        clusters = []
        for v_key, data in village_map.items():
            case_count = len(data["cases"])
            if case_count == 0:
                continue
            confirmed_count = sum(1 for c in data["cases"] if c.is_confirmed)
            avg_risk = sum(c.multimodal_risk_score for c in data["cases"]) / max(1, case_count)
            high_risk_count = sum(1 for c in data["cases"] if c.multimodal_risk_score >= 60)

            # Dominant condition
            conditions = [c.confirmed_condition or c.ai_predicted_condition for c in data["cases"]]
            dom_condition = max(set(conditions), key=conditions.count) if conditions else "None"

            # Dominant crop
            crops = [c.crop.name for c in data["cases"] if c.crop]
            dom_crop = max(set(crops), key=crops.count) if crops else "Tomato"

            tier = "Moderate"
            if avg_risk >= 70 or confirmed_count >= 5:
                tier = "Severe Hotspot"
            elif avg_risk >= 50:
                tier = "High Hotspot"

            clusters.append({
                "village": data["village"],
                "mandal": data["mandal"],
                "district": data["district"],
                "latitude": data["lat"],
                "longitude": data["lon"],
                "total_cases": case_count,
                "confirmed_cases": confirmed_count,
                "high_risk_count": high_risk_count,
                "average_risk_score": round(avg_risk, 1),
                "dominant_condition": dom_condition,
                "dominant_crop": dom_crop,
                "hotspot_tier": tier,
                "active_traps": len(data["traps"])
            })

        # Sort by average risk descending
        clusters.sort(key=lambda x: x["average_risk_score"], reverse=True)
        return clusters

gis_service = GISService()
