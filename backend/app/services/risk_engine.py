def calculate_risk(data: dict):
    score = 0
    factors = []

    temperature = data["temperature"]
    smoke = data["smoke"]
    gas = data["gas"]
    occupancy = data["occupancy"]

    if temperature >= 80:
        score += 35
        factors.append("Critical temperature")
    elif temperature >= 50:
        score += 20
        factors.append("Elevated temperature")

    if smoke >= 70:
        score += 40
        factors.append("Critical smoke concentration")
    elif smoke >= 30:
        score += 20
        factors.append("Elevated smoke concentration")

    if gas >= 15:
        score += 20
        factors.append("Abnormal gas level")

    if occupancy >= 80:
        score += 10
        factors.append("High occupancy")

    if data["status"] in ("OFFLINE", "FAULT"):
        score += 10
        factors.append(f"Sensor communication state: {data['status']}")

    score = min(score, 100)

    if score >= 80:
        band = "CRITICAL"
    elif score >= 60:
        band = "HIGH"
    elif score >= 40:
        band = "ELEVATED"
    elif score >= 20:
        band = "CAUTION"
    else:
        band = "NORMAL"

    return {
        "score": score,
        "band": band,
        "factors": factors,
        "zone": data["zone"],
    }
