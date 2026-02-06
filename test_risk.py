from risk_engine import calculate_risk, risk_category

sample_user = {
    "age": 52,
    "bmi": 32,
    "HbA1c_level": 7.2,
    "blood_glucose_level": 210,
    "hypertension": 1,
    "heart_disease": 0,
    "smoking_history": 2
}

score, reasons = calculate_risk(sample_user)
category = risk_category(score)

print("Risk Score:", score)
print("Risk Category:", category)
print("Reasons:", reasons)
