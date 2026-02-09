# group-project
![CI](https://img.shields.io/badge/tests-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.12-blue)
![ML](https://img.shields.io/badge/ML-XGBoost-orange)
![Explainability](https://img.shields.io/badge/Explainable-SHAP-purple)

🛡️ HealthGuard AI

Preventive Health Risk & Diabetes Clinical Decision Support System
Hackathon Project | AI for Healthcare | Clinical-Grade Risk Assessment

📌 Overview

HealthGuard AI is an AI-assisted preventive healthcare system designed to identify early health risks and provide clinical decision support using a hybrid approach:

1.Rule-based medical risk scoring (transparent & interpretable)
2.Machine Learning–based diabetes prediction (probabilistic & calibrated)
3.Explainable AI (SHAP) for trust and accountability
4.Human-centered design for doctors, patients, and caregivers

The system focuses on prevention, early intervention, and safe escalation, aligning with real-world hospital workflows.

🎯 Problem Statement Addressed

Modern healthcare systems often:
1.Detect disease too late
2.Over-rely on black-box AI
3.Lack explainability and trust

HealthGuard AI solves this by:
1.Surfacing early warning signs from routine patient data
2.Combining medical rules with AI (Human + Machine)
3.Ensuring AI can only escalate risk, never downgrade it
4.Providing clear explanations and actionable recommendations

🧠 System Architecture

User Input
   ↓
Rule-Based Risk Engine  ──► Base Health Risk (Green / Yellow / Orange / Red)
   ↓
ML Diabetes Prediction ──► Probability (%) + SHAP Explanation
   ↓
Safety Logic
   └─► ML can ONLY escalate risk (hospital-grade rule)
   ↓
Final Clinical Decision

🔬 Key Features

✅ 1. Rule-Based Health Risk Engine

A.Uses medically interpretable thresholds:
  (a)Age
  (b)BMI
  (c)HbA1c
  (d)Blood Glucose
  (e)Hypertension
  (f)Heart Disease
  (g)Smoking History
B.Produces:
  Risk Score (0–100)
  Risk Category:
       🟢 Green – Low Risk
       🟡 Yellow – Moderate Risk
       🟠 Orange – High Risk
       🔴 Red – Critical Risk
📁 File: risk_engine.py

🤖 2. Machine Learning Diabetes Prediction

Model: XGBoost (GPU-optimized)
Output:
    Calibrated probability (0–100%)
    Binary prediction only for escalation logic

Threshold optimized for:
     High Recall (patient safety first)

📁 Files:
models/ml_diabetes_train.py
models/ml_diabetes_predict.py
models/diabetes_model.pkl
models/diabetes_threshold.json

🧠 3. Explainable AI (SHAP) 

Shows top contributing features for each prediction
Uses raw XGBoost model (SHAP-compatible)
Prevents black-box decisions

📁 Files:
models/shap_explainer.py
models/shap_summary.png

🛑 4. Hospital-Grade Safety Logic

ML can ONLY escalate risk — never downgrade it
Example:
       Rule-based risk = 🟡 Yellow
       ML diabetes probability ≥ threshold
       👉 Final risk escalates to 🔴 Red
This mirrors real clinical decision-support systems.

📊 5. Streamlit Clinical Dashboard

Clean, intuitive UI
Separate sections for:
     Patient input
     Health risk summary
     Diabetes prediction
     Explainability
     Preventive recommendations
     Emergency mode (SMS alerts)

📁 File: app.py

🧪 Testing & Validation

Automated Tests
    Located in /tests:
         test_risk.py
         test_diabetes_prediction.py
         test_threshold_logic.py
         test_sms.py

Manual Validation
    Edge cases tested:
         Normal vitals but diabetic
         High HbA1c with normal glucose
         Conflicting rule vs ML outcomes

📁 Project Structure

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
│   ├── diabetes_threshold.json
│   ├── ml_diabetes_train.py
│   ├── ml_diabetes_predict.py
│   ├── shap_explainer.py
│   └── shap_summary.png
│
├── tests/
│   ├── test_risk.py
│   ├── test_diabetes_prediction.py
│   ├── test_threshold_logic.py
│   └── test_sms.py
│
├── app.py
├── risk_engine.py
├── sms_service.py
├── requirements.txt
└── README.md

🚀 How to Run the Project:

1️⃣ Install Dependencies
pip install -r requirements.txt

2️⃣ Launch Application
streamlit run app.py

📈 Example Output Interpretation:

Component	Meaning
Risk Score: 25	                                            Low rule-based risk
Risk Category: Green	                                    Preventive care recommended
Diabetes Risk: 21.44%	                                    Moderate probability (not diabetic yet)
SHAP Output	                                                Shows why the model predicted this

⚠️ Medical Disclaimer

This system is an AI-assisted screening and decision-support tool.
It does NOT replace professional medical diagnosis or treatment.
Final clinical decisions must always be made by qualified healthcare professionals.

🏆 Why This Project Stands Out

✔ Human + AI collaboration
✔ Explainable & transparent
✔ Clinically realistic logic
✔ Patient-safety focused
✔ Hackathon-ready & scalable

👨‍⚕️ Future Enhancements

CI/CD integration
EHR/FHIR compatibility
Multi-disease prediction
Personalized lifestyle plans
Doctor-facing analytics dashboard

🙌 Team & Credits

Built with ❤️ for preventive healthcare using:
Python
Streamlit
XGBoost
SHAP
Scikit-learn

🛡️ HealthGuard AI

Prevention • Prediction • Protection