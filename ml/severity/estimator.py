from typing import Dict, Any

class SeverityEstimator:
    """
    Quantifies foliage disease severity by assessing necrotic/chlorotic lesion
    area relative to total leaf blade surface.
    """

    @staticmethod
    def classify_severity(percentage_damage: float) -> str:
        if percentage_damage < 15.0:
            return "Mild"
        elif percentage_damage <= 40.0:
            return "Moderate"
        else:
            return "Severe"

    @staticmethod
    def estimate(
        percentage_damage: float = 28.5,
        canopy_spread: str = "Lower leaves only"
    ) -> Dict[str, Any]:
        severity = SeverityEstimator.classify_severity(percentage_damage)
        urgency = "Normal"
        if severity == "Moderate":
            urgency = "Urgent"
        elif severity == "Severe":
            urgency = "Critical Immediate Action"

        return {
            "severity_level": severity,
            "percentage_damage": round(percentage_damage, 1),
            "canopy_spread": canopy_spread,
            "urgency": urgency,
            "requires_canopy_sanitation": percentage_damage > 20.0
        }

severity_estimator = SeverityEstimator()
