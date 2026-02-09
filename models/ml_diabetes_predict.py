import joblib
import json
import numpy as np
import shap
import pandas as pd

def validate_inputs(user_data):
    warnings = []

    if not (1 <= user_data["age"] <= 120):
        raise ValueError("Age must be between 1 and 120")

    if not (10 <= user_data["bmi"] <= 60):
        warnings.append("BMI value is outside normal clinical range")

    if not (3 <= user_data["HbA1c_level"] <= 15):
        warnings.append("HbA1c value is unusual")

    if not (50 <= user_data["blood_glucose_level"] <= 500):
        raise ValueError("Blood glucose value is invalid")

    return warnings

# Load artifacts once
model = joblib.load("models/diabetes_model.pkl")
imputer = joblib.load("models/diabetes_imputer.pkl")
feature_columns = joblib.load("models/diabetes_features.pkl")

with open("models/diabetes_threshold.json") as f:
    THRESHOLD = json.load(f)["threshold"]

# Calibrated model (for probability)
model = joblib.load("models/diabetes_model.pkl")

# Raw model (for SHAP)
raw_model = joblib.load("models/diabetes_model_raw.pkl")

explainer = shap.TreeExplainer(raw_model)


def predict_diabetes(user_data):
    warnings = validate_inputs(user_data)
    # Convert to DataFrame
    X = pd.DataFrame([user_data], columns=feature_columns)

    # Impute
    X_imputed = imputer.transform(X)

    # Predict
    proba = model.predict_proba(X_imputed)[0][1]
    prediction = int(proba >= THRESHOLD)

    # SHAP values
    shap_values = explainer.shap_values(X)

    shap_result = dict(
        sorted(
            zip(feature_columns, shap_values[0]),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:5]  # top 5 contributors
    )

    return prediction, round(proba * 100, 2), shap_result, warnings

from models.shap_explainer import explain_prediction
import joblib
import numpy as np

# Load feature order used during training
feature_columns = joblib.load("models/diabetes_features.pkl")

def predict_diabetes_full(user_data):
    """
    Returns:
    prediction, probability, shap_explanation, warnings
    """

    prediction, probability, _, _ = predict_diabetes(user_data)

    warnings = []

    if user_data["HbA1c_level"] >= 6.5:
        warnings.append("HbA1c above diagnostic threshold")

    if user_data["blood_glucose_level"] >= 140:
        warnings.append("High blood glucose level")

    if user_data["bmi"] >= 30:
        warnings.append("Obesity risk")

     # SHAP (correct feature order)
    X = pd.DataFrame([user_data], columns=feature_columns)
    X = imputer.transform(X)
    raw_shap = explain_prediction(X, feature_columns)

    # Convert list → dict safely
    shap_info = dict(raw_shap)

    return prediction, probability, shap_info, warnings

# ============================================================
# HOSPITAL-GRADE DIABETES PREDICTION PIPELINE
# ============================================================
