🛡️ HealthGuard AI

Preventive Health Risk & Diabetes Clinical Decision Support System
Hackathon Project | AI for Healthcare | Clinical-Grade Risk Intelligence Platform

📌 Overview

HealthGuard AI is a hybrid preventive healthcare intelligence system designed to:
(a) Detect early health deterioration
(b) Predict diabetes risk using calibrated ML
(c) Provide explainable AI outputs (SHAP)
(d) Generate personalized AI-driven intervention plans
(e) Escalate safely using hospital-grade logic

The system combines:
(1) Rule-Based Clinical Risk Engine
(2) XGBoost ML Diabetes Predictor
(3) SHAP Explainability
(4) Advanced Personalized Intervention Engine
(5) User Authentication & Health History Tracking
(6) Emergency Escalation with SMS Alerts

This mirrors real-world Clinical Decision Support Systems (CDSS).

🎯 Problem Statement

Modern healthcare systems:
(A) Detect disease too late
(B) Over-rely on black-box AI
(C) Lack patient-specific preventive guidance
(D) Provide generic lifestyle advice
(E) Do not enforce safe escalation logic

HealthGuard AI solves this by:
✔ Combining medical logic + AI
✔ Allowing ML to escalate but never downgrade risk
✔ Generating personalized diet & exercise plans
✔ Tracking patient longitudinal history
✔ Maintaining explainability & accountability

🧠 System Architecture

User Input
   ↓
Rule-Based Risk Engine  ──► Base Health Risk
   ↓
ML Diabetes Prediction ──► Calibrated Probability (%)
   ↓
Explainability Engine (SHAP)
   ↓
Safety Logic (Escalation Only)
   ↓
Final Clinical Risk Category
   ↓
Advanced Intervention Engine
   ├─ Personalized Diet Plan
   ├─ Weekly Workout Plan
   ├─ Yoga Protocol
   ├─ Calorie & Protein Targets
   └─ Precautions

🔬 Core System Modules

✅ 1. Rule-Based Clinical Risk Engine

📁 risk_engine.py

Uses medically interpretable thresholds:
1) Age
2) BMI
3) HbA1c
4) Blood Glucose
5) Hypertension
6) Heart Disease
7) Smoking History

Outputs:
(A) Risk Score (0–100)
(B) Risk Category:
                 🟢 Green – Low
                 🟡 Yellow – Moderate
                 🟠 Orange – High
                 🔴 Red – Critical
Transparent and fully interpretable.

🤖 2. Machine Learning Diabetes Prediction

📁 models/ml_diabetes_predict.py
📁 models/diabetes_model.pkl

Model: XGBoost (GPU optimized)
Outputs:
(a) Calibrated probability (%)
(b) Binary prediction (for escalation logic)
(c) SHAP feature contributions
Optimized for high recall (patient safety first).

🧠 3. Explainable AI (SHAP)

📁 models/shap_explainer.py
📁 models/shap_summary.png

(a) Shows top contributing features
(b) Prevents black-box decisions
(c) Enables transparency for judges & clinicians

🛑 4. Hospital-Grade Safety Logic

ML can ONLY escalate risk — never downgrade it.
Example:

---> Rule Risk = 🟡 Yellow
     ML Probability ≥ Critical Threshold
     👉 Final Risk = 🔴 Red

This mirrors real clinical escalation workflows.

🧬 5. Advanced Intervention Engine

📁 intervention_engine.py
📁 advanced_intervention_engine.py

This module generates personalized health plans, including:

🔹 Calorie Calculation

(a) BMR-based (Mifflin-St Jeor)
(b) BMI-adjusted
(c) Risk-adjusted calorie targets

🔹 Macronutrient Planning

(a) Protein target (grams)
(b) Carbohydrate adjustment for glucose risk
(c) Heart-safe fat modulation

🔹 Weekly Workout Plan

(a) Risk-adjusted intensity
(b) Heart-safe protocols
(c) Age-modified training
(d) Obesity-safe progression

🔹 Personalized Yoga Plan

(a) Hypertension-safe breathing
(b) Cardio-protective poses
(c) Stress reduction sequencing

🔹 Ramadan Mode (Adaptive Logic)

(a) Calorie redistribution
(b) Hydration strategy
(c) Safe fasting modifications

🔹 BMI → Body Fat Estimation

(a) Predictive estimation
(b) Obesity risk mapping
This transforms the system into a preventive metabolic optimization platform.

🔐 6. Authentication & User System

📁 auth.py
📁 users.json

Features:
1) Email login
2) Numeric password system
3) "Remember Me" session persistence
4) Multi-user support
5) Primary user tracking
6) Auto-login on same device
7) Personal health history storage

📈 7. Longitudinal Health Tracking

Each user has:
1) Historical risk scores
2) Historical diabetes probabilities
3) Trend visualization (line charts)
4) Complete health check history
5) Expandable medical records

This enables longitudinal monitoring — not just one-time screening.

🚨 8. Emergency Mode & SMS Alerts

📁 sms_service.py

When risk is 🔴 Red:

1) Emergency hospital recommendation
2) Google Maps link
3) Optional caretaker SMS alert

📊 Dashboard (Streamlit)

📁 app.py

Includes:

• 🔐 Login / Signup
• 🩺 Health Check tab
• 📈 History Tab
• 🧠 Personalized AI Plan Tab
• 📊 Risk Visualization
• 📉 Trend Analytics
• 🚨 Emergency Mode
Clean, clinical UI design.

📁 Updated Project Structure

GROUP-PROJECT/
│
├── DATA/
│   └── diabetes_dataset.csv
│
├── models/
│   ├── diabetes_model.pkl
│   ├── diabetes_model_raw.pkl
│   ├── diabetes_imputer.pkl
│   ├── diabetes_features.pkl
│   ├── diabetes_scaler.pkl
│   ├── diabetes_threshold.json
│   ├── diabetes_risk_mapper.py
│   ├── ml_data_prepare.py
│   ├── ml_diabetes_train.py
│   ├── ml_diabetes_predict.py
│   ├── shap_explainer.py
│   └── shap_summary.png
│
├── tests/
│   ├── test_risk.py
│   ├── test_ml_diabetes.py
│   ├── test_sms.py
│   └── test_data.py
│
├── app.py
├── risk_engine.py
├── intervention_engine.py
├── advanced_intervention_engine.py
├── preprocess.py
├── auth.py
├── sms_service.py
├── users.json
├── requirements.txt
└── README.md

🚀 How to Run

1️⃣ Install Dependencies
pip install -r requirements.txt

2️⃣ Launch Application
streamlit run app.py

📈 Example Output

| Component                 | Meaning                               |
| ------------------------- | ------------------------------------- |
| Risk Score: 42            | Moderate rule-based risk              |
| Risk Category: Yellow     | Preventive intervention required      |
| Diabetes Probability: 68% | Elevated metabolic risk               |
| SHAP Output               | Shows HbA1c & BMI as dominant drivers |
| Personalized Plan         | Risk-adjusted diet + workout + yoga   |

🏥 Clinical Realism

✔ Transparent rule logic
✔ ML calibration
✔ Escalation-only override
✔ Patient-safety-first thresholding
✔ Longitudinal monitoring
✔ Personalized metabolic strategy

🧪 Testing

Located in /tests:
• Rule engine validation
• ML probability validation
• Threshold safety logic
• SMS service testing
• Data pipeline tests

🏆 Why This Project Is Advanced

✔ Hybrid AI (Rules + ML)
✔ Explainable AI
✔ Escalation Safety Logic
✔ Personalized metabolic modeling
✔ User-based longitudinal tracking
✔ Emergency escalation
✔ Hackathon-ready yet scalable

🔮 Future Enhancements

• EHR / FHIR Integration
• Multi-disease prediction (CVD, CKD, NAFLD)
• AI Doctor Dashboard
• App Version
• Cloud Deployment (AWS/GCP)
• CI/CD Pipeline
• Clinical Trial Simulation

⚠️ Medical Disclaimer

This system is an AI-assisted screening and decision-support tool.
It does NOT replace professional medical diagnosis or treatment.
All medical decisions must be made by licensed healthcare professionals.