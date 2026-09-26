from typing import List, Dict, Any
from datetime import datetime, timedelta

class EpidemicRiskForecaster:
    """
    Microclimate-driven epidemiological forecaster.
    Predicts disease progression and spatial risk probability over 24-hour,
    3-day, and 7-day horizons based on atmospheric trends and pathogen persistence.
    """

    def forecast_trajectory(
        self,
        current_risk: float,
        rainfall_expected_3d_mm: float = 24.0,
        humidity_trend: str = "High",
        nearby_cases: int = 6
    ) -> List[Dict[str, Any]]:
        """
        Generates 7-day daily risk curve.
        """
        forecasts = []
        today = datetime.utcnow()

        # Progression multiplier based on moisture persistence
        if humidity_trend == "High" and rainfall_expected_3d_mm > 15:
            trend_multiplier = 1.04  # Accelerating
        elif humidity_trend == "Moderate":
            trend_multiplier = 1.00  # Plateau
        else:
            trend_multiplier = 0.95  # Decaying

        simulated_risk = current_risk
        for day in range(1, 8):
            target_date = today + timedelta(days=day)
            # Apply dynamic progression with natural saturation at 98
            simulated_risk = min(98.0, max(10.0, simulated_risk * (trend_multiplier ** (1.0 / (day ** 0.5)))))
            
            if simulated_risk >= 76:
                tier = "Very High"
            elif simulated_risk >= 51:
                tier = "High"
            elif simulated_risk >= 26:
                tier = "Moderate"
            else:
                tier = "Low"

            action = "Continue weekly scouting."
            if simulated_risk >= 75:
                action = "Pre-emptive IPM intervention recommended before sporulation."
            elif simulated_risk >= 50:
                action = "Inspect lower canopy daily and ensure drainage channels are clear."

            forecasts.append({
                "day_offset": day,
                "date": target_date.strftime("%Y-%m-%d"),
                "predicted_risk_score": round(simulated_risk, 1),
                "risk_tier": tier,
                "expected_rain_mm": round(max(0.0, rainfall_expected_3d_mm * (0.8 ** day)), 1),
                "recommended_action": action
            })

        return forecasts

epidemic_forecaster = EpidemicRiskForecaster()
