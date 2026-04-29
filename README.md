# HealthGuard AI

# HealthGuard AI

![Python](https://img.shields.io/badge/python-3.12-blue)
![Model](https://img.shields.io/badge/model-XGBoost-orange)
![Framework](https://img.shields.io/badge/framework-Streamlit-green)

AI-powered preventive healthcare system for health risk assessment, diabetes prediction, and personalized intervention planning.

## Overview

HealthGuard AI is a clinical decision-support system designed to assess health risk and predict diabetes using a hybrid architecture combining rule-based logic and machine learning.

The system evaluates user health data, generates a risk score, predicts diabetes probability, explains model decisions, and provides personalized health recommendations including diet, exercise, and emergency escalation for critical cases.

## Features

- Health risk scoring
- Diabetes prediction using XGBoost
- Explainable AI using SHAP
- Personalized diet planning
- Exercise recommendations
- Yoga guidance
- User authentication and history tracking
- Emergency hospital recommendations
- SMS alert support

## System Architecture

```text
User Input
   │
   ├── Rule-Based Risk Engine
   │
   ├── Diabetes Prediction Model
   │
   ├── Explainability Layer (SHAP)
   │
   ├── Risk Escalation Logic
   │
   └── Personalized Intervention Engine
```

## Core Modules

### Risk Engine
Evaluates user health data using clinical thresholds such as:

- Age
- BMI
- Blood glucose
- HbA1c
- Hypertension
- Heart disease
- Smoking history

Outputs:
- Risk score (0–100)
- Risk category (Low, Moderate, High, Critical)

---

### Machine Learning Model
Uses XGBoost for diabetes prediction.

Outputs:
- Probability score
- Risk classification
- Feature contribution analysis

---

### Explainability Layer
SHAP is used to provide model transparency by showing feature importance and contribution.

---

### Intervention Engine
Generates personalized plans based on user health data:

- Daily calorie targets
- Macronutrient planning
- Weekly workout plans
- Yoga recommendations
- Lifestyle precautions

---

### Emergency System
In critical cases, the system can:

- Recommend hospitals
- Provide location support
- Send emergency SMS alerts

## Dashboard

The application includes:

- User login and signup
- Health assessment dashboard
- Historical reports
- Risk visualization
- Personalized health plans
- Emergency recommendations

## Screenshots

### Dashboard
<img width="1514" height="821" alt="55ba06d3-0d5d-4513-bc6f-34609c261e77" src="https://github.com/user-attachments/assets/d175664e-4b57-4489-8ff6-4c4d9d64a93e" />


### Health Assessment Report
<img width="1363" height="491" alt="56a4d087-d68f-478b-9aa9-86dcdc364d01" src="https://github.com/user-attachments/assets/c1ca2830-1906-4531-9fb3-88cc13a86822" />


### Personalized Recommendation Panel
<img width="1507" height="825" alt="44c3e1b0-a10c-4b1b-8891-fefa91b5bef6" src="https://github.com/user-attachments/assets/c8f29c7d-b96e-42b9-b140-e44e7ee90c67" />


## Tech Stack

- Python
- XGBoost
- SHAP
- Streamlit
- Scikit-learn
- Pandas

## Project Structure

```text
data/
models/
tests/
app.py
risk_engine.py
intervention_engine.py
auth.py
sms_service.py
requirements.txt
README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
streamlit run app.py
```

## Future Improvements

- Multi-disease prediction
- Doctor dashboard integration
- Cloud deployment
- Mobile application
- API integration

## Disclaimer

This project is an AI-assisted health screening and decision-support system intended for educational and preventive purposes only. It should not be used as a substitute for professional medical diagnosis or treatment.
