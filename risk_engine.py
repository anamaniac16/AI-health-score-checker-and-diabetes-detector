def calculate_risk(data):
    """
    data = dictionary containing user health values
    """

    risk_score = 0
    reasons = []

    # Age risk
    if data["age"] > 45:
        risk_score += 10
        reasons.append("Age above 45")

    # BMI risk
    if data["bmi"] > 30:
        risk_score += 15
        reasons.append("High BMI")

    # HbA1c risk
    if data["HbA1c_level"] > 6.5:
        risk_score += 25
        reasons.append("High HbA1c level")

    # Blood glucose risk
    if data["blood_glucose_level"] > 180:
        risk_score += 25
        reasons.append("High blood glucose")

    # Hypertension
    if data["hypertension"] == 1:
        risk_score += 15
        reasons.append("Hypertension")

    # Heart disease
    if data["heart_disease"] == 1:
        risk_score += 20
        reasons.append("Heart disease history")

    # Smoking
    if data["smoking_history"] == 2:  # current smoker
        risk_score += 10
        reasons.append("Current smoker")

    return risk_score, reasons

def risk_category(score):
    if score <= 30:
        return "Green (Low Risk)"
    elif score <= 50:
        return "Yellow (Moderate Risk)"
    elif score <= 70:
        return "Orange (High Risk)"
    else:
        return "Red (Critical Risk)"
