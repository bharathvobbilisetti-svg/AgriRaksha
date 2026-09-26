import math
from typing import Dict, Any, Optional
import httpx

class WeatherRiskEngine:
    """
    Agro-meteorological disease forecasting engine.
    Applies empirical microclimate thresholds and the Wallin Disease Severity Value (DSV)
    for fungal spore germination, hyphal elongation, and bacteriological proliferation.
    Supports real-time Open-Meteo microclimate retrieval with offline fallback.
    """

    @staticmethod
    def fetch_live_weather(lat: float = 17.6868, lon: float = 83.2185) -> Optional[Dict[str, Any]]:
        """
        Retrieves real-time agro-meteorological parameters from Open-Meteo API.
        Zero API keys required. Fallbacks to None if network is unavailable.
        """
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&"
            f"current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m&"
            f"hourly=dew_point_2m,precipitation_probability&forecast_days=3"
        )
        try:
            with httpx.Client(timeout=2.5) as client:
                resp = client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    curr = data.get("current", {})
                    temp = float(curr.get("temperature_2m", 25.0))
                    rh = float(curr.get("relative_humidity_2m", 80.0))
                    rain = float(curr.get("precipitation", 0.0))
                    wind = float(curr.get("wind_speed_10m", 8.0))

                    # Hourly forecast probabilities
                    hourly = data.get("hourly", {})
                    rain_probs = hourly.get("precipitation_probability", [40.0])
                    p24 = float(max(rain_probs[:24])) if len(rain_probs) >= 24 else 45.0
                    p72 = float(max(rain_probs[:72])) if len(rain_probs) >= 72 else 60.0

                    # Estimated leaf wetness: RH > 85% or dew point proximity
                    dew_pts = hourly.get("dew_point_2m", [temp - 2.0])
                    dew_depression = temp - (dew_pts[0] if dew_pts else (temp - 2.0))
                    if dew_depression < 1.5 or rh > 85.0:
                        leaf_wetness = 6.0
                    elif dew_depression < 3.0 or rh > 75.0:
                        leaf_wetness = 3.5
                    else:
                        leaf_wetness = 1.0

                    condition = "Humid / Overcast" if rh > 75 else "Partly Cloudy"
                    if rain > 2.0:
                        condition = "Rain Showers"

                    return {
                        "latitude": lat,
                        "longitude": lon,
                        "temperature_c": temp,
                        "relative_humidity_pct": rh,
                        "rainfall_mm": rain,
                        "leaf_wetness_hours": leaf_wetness,
                        "wind_speed_kmh": wind,
                        "forecast_rain_prob_24h": p24,
                        "forecast_rain_prob_72h": p72,
                        "weather_condition": condition,
                        "icon": "cloud-rain" if (rain > 0 or rh > 80) else "sun"
                    }
        except Exception:
            return None

    def calculate_wallin_dsv(
        self,
        temperature_c: float,
        relative_humidity_pct: float,
        leaf_wetness_hours: float
    ) -> int:
        """
        Wallin Disease Severity Value (DSV) for Late/Early Blight.
        Returns DSV index from 0 (no risk) to 4 (maximum epidemic pressure).
        """
        if relative_humidity_pct < 75.0 and leaf_wetness_hours < 3.0:
            return 0
        if 13.0 <= temperature_c <= 29.0:
            if leaf_wetness_hours >= 8.0 or relative_humidity_pct >= 90.0:
                return 4
            elif leaf_wetness_hours >= 5.0 or relative_humidity_pct >= 85.0:
                return 3
            elif leaf_wetness_hours >= 3.0 or relative_humidity_pct >= 80.0:
                return 2
            else:
                return 1
        return 1

    def calculate_weather_risk(
        self,
        temperature_c: float,
        relative_humidity_pct: float,
        rainfall_mm: float,
        leaf_wetness_hours: float = 2.0,
        wind_speed_kmh: float = 8.0,
        condition_target: str = "Early Blight"
    ) -> Dict[str, Any]:
        """
        Calculates normalized weather suitability index (0 - 100) and Wallin DSV.
        """
        score = 20.0  # Base ambient risk

        # Relative Humidity contribution (up to +35 pts)
        if relative_humidity_pct >= 85:
            score += 35
        elif relative_humidity_pct >= 75:
            score += 25
        elif relative_humidity_pct >= 60:
            score += 15
        else:
            score += 5

        # Leaf wetness contribution (up to +25 pts)
        if leaf_wetness_hours >= 6.0:
            score += 25
        elif leaf_wetness_hours >= 4.0:
            score += 18
        elif leaf_wetness_hours >= 2.0:
            score += 10

        # Rainfall contribution (up to +20 pts)
        if rainfall_mm >= 15.0:
            score += 20
        elif rainfall_mm >= 5.0:
            score += 14
        elif rainfall_mm > 0.0:
            score += 8

        # Temperature suitability window (20 - 30 C is prime for fungal pathogens)
        if 20 <= temperature_c <= 30:
            score += 15
        elif 16 <= temperature_c <= 34:
            score += 8

        weather_score = min(100.0, max(5.0, score))

        if weather_score >= 76:
            category = "Very High"
        elif weather_score >= 51:
            category = "High"
        elif weather_score >= 26:
            category = "Moderate"
        else:
            category = "Low"

        # Calculate Wallin DSV
        dsv = self.calculate_wallin_dsv(temperature_c, relative_humidity_pct, leaf_wetness_hours)

        # Key meteorological drivers
        drivers = []
        if relative_humidity_pct >= 75:
            drivers.append(f"Elevated relative humidity ({relative_humidity_pct:.1f}%) creates ideal spore incubation environment")
        if leaf_wetness_hours >= 4:
            drivers.append(f"Prolonged leaf wetness ({leaf_wetness_hours:.1f} hrs) accelerates pathogen penetration")
        if rainfall_mm > 5:
            drivers.append(f"Recent rainfall ({rainfall_mm:.1f} mm) causes splash dispersal of soil-borne inoculum")
        if 20 <= temperature_c <= 30:
            drivers.append(f"Ambient temperature ({temperature_c:.1f}°C) falls inside optimal thermal growth range")

        return {
            "weather_suitability_score": round(weather_score, 1),
            "category": category,
            "wallin_dsv": dsv,
            "drivers": drivers,
            "spore_germination_risk": round(weather_score * 0.95, 1)
        }


weather_risk_engine = WeatherRiskEngine()
