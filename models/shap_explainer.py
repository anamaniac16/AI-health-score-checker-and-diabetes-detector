import joblib
import shap
import numpy as np

# Load RAW (non-calibrated) model
raw_model = joblib.load("models/diabetes_model_raw.pkl")

# SHAP explainer (Tree-based)
explainer = shap.TreeExplainer(raw_model)

def explain_prediction(X, feature_names, top_k=5):
    """
    Returns top contributing features with direction
    """

    shap_values = explainer.shap_values(X)

    # SHAP values for single sample
    shap_vals = shap_values[0]

    # Sort by absolute impact
    sorted_features = sorted(
        zip(feature_names, shap_vals),
        key=lambda x: abs(x[1]),
        reverse=True
    )

    # Return top-k as dict (feature -> signed impact)
    return dict(sorted_features[:top_k])
