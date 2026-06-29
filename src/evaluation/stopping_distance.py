import math

# Default parameters (can be adjusted)
DEFAULT_REACTION_TIME = 1.5  # seconds
DEFAULT_DECELERATION = 5.0   # m/s^2 (approx. typical comfortable deceleration)

def risk_level(pri: float) -> str:
    """Return risk level based on PRI thresholds.
    HIGH risk → PRI < 1.0
    MODERATE risk → 1.0 <= PRI < 1.5
    LOW risk → PRI >= 1.5
    """
    if pri < 1.0:
        return "HIGH"
    if pri < 1.5:
        return "MODERATE"
    return "LOW"

def recommended_speed(risk: str) -> int:
    """Map risk level to a safe speed (km/h)."""
    mapping = {
        "HIGH": 20,
        "MODERATE": 40,
        "LOW": 60,
    }
    return mapping.get(risk.upper(), 60)

def stopping_distance(speed_kmh: int, reaction_time: float = DEFAULT_REACTION_TIME, deceleration: float = DEFAULT_DECELERATION):
    """Calculate reaction, braking, and total stopping distance.
    speed_kmh: vehicle speed in km/h.
    reaction_time: driver reaction time in seconds.
    deceleration: braking deceleration in m/s^2.
    Returns a dict with distances in meters.
    """
    speed_ms = speed_kmh / 3.6  # convert to m/s
    reaction_distance = speed_ms * reaction_time
    braking_distance = (speed_ms ** 2) / (2 * deceleration) if deceleration != 0 else math.inf
    total = reaction_distance + braking_distance
    return {
        "reaction_distance": reaction_distance,
        "braking_distance": braking_distance,
        "stopping_distance": total,
    }

def summarize(fog_density: str, detection_count: float, avg_confidence: float, pri: float, reaction_time: float = DEFAULT_REACTION_TIME, deceleration: float = DEFAULT_DECELERATION):
    """Produce a safety summary dictionary for a given fog density.
    Returns keys: risk, speed, reaction_distance, braking_distance, stopping_distance, text.
    """
    risk = risk_level(pri)
    speed = recommended_speed(risk)
    distances = stopping_distance(speed, reaction_time, deceleration)
    interpretation = {
        "HIGH": "Perception degradation – high risk",
        "MODERATE": "Minimal recovery – moderate risk",
        "LOW": "Strong recovery – low risk",
    }[risk]
    text = (
        f"{fog_density} fog: PRI={pri:.2f} ({interpretation}). "
        f"Recommended speed: {speed} km/h. "
        f"Stopping distance ≈ {distances['stopping_distance']:.1f} m (reaction {distances['reaction_distance']:.1f} m, braking {distances['braking_distance']:.1f} m)."
    )
    return {
        "risk": risk,
        "speed": speed,
        "reaction_distance": distances["reaction_distance"],
        "braking_distance": distances["braking_distance"],
        "stopping_distance": distances["stopping_distance"],
        "text": text,
    }

if __name__ == "__main__":
    # Demo with placeholder values for each density
    for fog in ["No_Fog", "Medium_Fog", "Dense_Fog"]:
        # Example values – in real use these come from the analysis summary
        demo_pri = 0.8 if fog == "Dense_Fog" else 2.0
        result = summarize(fog, detection_count=0, avg_confidence=0, pri=demo_pri)
        print(result["text"])
