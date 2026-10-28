# app/services/metrics.py

def calculate_bmi(height_cm: float, weight_kg: float) -> float | None:
    """Cálculo exacto rescatado de DataMapper."""
    if not height_cm or not weight_kg or height_cm <= 0 or weight_kg <= 0:
        return None
    height_m = height_cm / 100.0
    return round(weight_kg / (height_m ** 2), 2)

TOBACCO_MAP = {
    "Never": 1,
    "Former": 2,
    "Current": 3
}

ALCOHOL_MAP = {
    "Never": 1,
    "Occasional": 2,
    "Regular": 3
}

SNORING_EVOLUTION_MAP = {
    "never": 0,
    "occasionally or continuously less than 2 years": 1,
    "occasionally or continuously for less than 2 years": 1,
    "continuously for more than 2 years": 2,
    "continuously for more than 5 years": 3,
}