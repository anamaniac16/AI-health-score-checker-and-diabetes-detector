# ============================================================
# HOSPITAL-GRADE DIABETES ML TRAINING PIPELINE
# ============================================================

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV

# ---------------- ML / SKLEARN ----------------
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# ---------------- XGBOOST ----------------
from xgboost import XGBClassifier

# ---------------- SHAP ----------------
import shap
import matplotlib.pyplot as plt


# ============================================================
# 1️⃣ LOAD DATA
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "DATA", "diabetes_dataset.csv")

df = pd.read_csv(DATA_PATH)

# Clean inconsistent strings
df.replace(["No Info", "Unknown", "none"], np.nan, inplace=True)


# ============================================================
# 2️⃣ FEATURE ENGINEERING
# ============================================================

categorical_cols = ["gender", "smoking_history"]

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))

# Split features and target
X = df.drop("diabetes", axis=1)
y = df["diabetes"]

feature_columns = X.columns.tolist()
joblib.dump(feature_columns, "models/diabetes_features.pkl")

# Impute missing values
imputer = SimpleImputer(strategy="median")
X = imputer.fit_transform(X)


# ============================================================
# 3️⃣ TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    stratify=y,
    random_state=42
)


# ============================================================
# 4️⃣ GPU-OPTIMIZED XGBOOST MODEL
# ============================================================

xgb = XGBClassifier(
    tree_method="hist",        # GPU-compatible
    eval_metric="auc",
    use_label_encoder=False,

    n_estimators=800,
    max_depth=6,
    learning_rate=0.03,
    subsample=0.85,
    colsample_bytree=0.85,
    gamma=0.1,
    min_child_weight=3,
    reg_alpha=0.1,
    reg_lambda=1.0,

    random_state=42
)

# 🔥 TRAIN ONCE (IMPORTANT)
xgb.fit(X_train, y_train)

# ============================================================
# 4️⃣.5 PROBABILITY CALIBRATION (CRITICAL)
# ============================================================

calibrated_model = CalibratedClassifierCV(
    xgb,
    method="sigmoid",   # ✅ Medical-grade calibration
    cv=5
)

calibrated_model.fit(X_train, y_train)

# ============================================================
# 5️⃣ PROBABILITY PREDICTIONS
# ============================================================

y_proba = calibrated_model.predict_proba(X_test)[:, 1]

# ============================================================
# 6️⃣ HOSPITAL-GRADE THRESHOLD OPTIMIZATION
# (Maximize Recall – patient safety first)
# ============================================================

thresholds = np.arange(0.20, 0.60, 0.02)

best_threshold = 0.50
best_recall = 0.0
best_f1 = 0.0

print("\n📊 Threshold Optimization Results")
print("-" * 50)

for t in thresholds:
    y_pred_custom = (y_proba >= t).astype(int)

    recall = recall_score(y_test, y_pred_custom)
    f1 = f1_score(y_test, y_pred_custom)

    print(f"Threshold {t:.2f} → Recall: {recall:.4f} | F1: {f1:.4f}")

    if recall > best_recall:
        best_threshold = t
        best_recall = recall
        best_f1 = f1

print("\n🏥 Hospital-Grade Threshold Selected")
print(f"Threshold : {best_threshold}")
print(f"Recall    : {best_recall}")
print(f"F1 Score  : {best_f1}")


# ============================================================
# 7️⃣ FINAL EVALUATION USING HOSPITAL THRESHOLD
# ============================================================

y_pred_final = (y_proba >= best_threshold).astype(int)

accuracy = accuracy_score(y_test, y_pred_final)
recall = recall_score(y_test, y_pred_final)
f1 = f1_score(y_test, y_pred_final)
roc = roc_auc_score(y_test, y_proba)

print("\n📊 FINAL MODEL PERFORMANCE (Hospital Threshold)")
print(f"Accuracy : {accuracy:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1-Score : {f1:.4f}")
print(f"ROC-AUC  : {roc:.4f}")


# ============================================================
# 8️⃣ CONFUSION MATRIX (Before vs After)
# ============================================================

# Default threshold
y_pred_default = (y_proba >= 0.50).astype(int)
cm_default = confusion_matrix(y_test, y_pred_default)

# Hospital threshold
cm_hospital = confusion_matrix(y_test, y_pred_final)

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

ConfusionMatrixDisplay(cm_default).plot(ax=ax[0], colorbar=False)
ax[0].set_title("Default Threshold (0.50)")

ConfusionMatrixDisplay(cm_hospital).plot(ax=ax[1], colorbar=False)
ax[1].set_title(f"Hospital Threshold ({best_threshold})")

plt.tight_layout()
plt.show()


# ============================================================
# 9️⃣ SAVE MODEL & THRESHOLD
# ============================================================

joblib.dump(calibrated_model, "models/diabetes_model.pkl")
joblib.dump(xgb, "models/diabetes_model_raw.pkl")
joblib.dump(imputer, "models/diabetes_imputer.pkl")

with open("models/diabetes_threshold.json", "w") as f:
    json.dump({"threshold": round(float(best_threshold), 2)}, f)

print("\n✅ GPU-Optimized XGBoost model saved successfully")
print(f"🏥 Hospital threshold saved: {best_threshold}")

# ============================================================
# 🔟 SHAP EXPLAINABILITY (OPTIONAL BUT 🔥)
# ============================================================

explainer = shap.TreeExplainer(xgb)
shap_values = explainer.shap_values(X_test)

shap.summary_plot(
    shap_values,
    X_test,
    feature_names=feature_columns
)
print("\n🧠 Generating SHAP explanations...")

# Load feature names
feature_columns = joblib.load("models/diabetes_features.pkl")

# Convert X_test back to DataFrame
X_test_df = pd.DataFrame(X_test, columns=feature_columns)

explainer = shap.TreeExplainer(xgb)
shap_values = explainer.shap_values(X_test_df)

# Summary plot (global importance)
shap.summary_plot(
    shap_values,
    X_test_df,
    show=False
)

plt.tight_layout()
plt.savefig("models/shap_summary.png")
plt.close()

print("✅ SHAP summary saved as models/shap_summary.png")