# HealthGuard AI

![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.12-blue)
![ML](https://img.shields.io/badge/ML-XGBoost-orange)

AI-powered health risk assessment system for diabetes prediction and preventive healthcare recommendations.

## Overview

HealthGuard AI is a healthcare intelligence system that evaluates a user’s health condition using clinical data and machine learning. It predicts diabetes risk, calculates a health score, and provides personalized recommendations based on the results.

In high-risk cases, the system can suggest hospitals and trigger emergency alerts.

## Features

• Health risk scoring  
• Diabetes prediction using XGBoost  
• Explainable predictions using SHAP  
• Personalized diet recommendations  
• Exercise planning  
• Health history tracking  
• Emergency hospital suggestions  
• SMS alert support  

## Tech Stack

- Python
- XGBoost
- SHAP
- Streamlit
- Pandas
- Scikit-learn

## Project Structure

```
app.py
risk_engine.py
intervention_engine.py
auth.py
sms_service.py
models/
tests/
README.md

```

How It Works
User enters health details
System calculates health risk score
ML model predicts diabetes probability
Risk level is generated
Personalized suggestions are provided
Critical cases trigger hospital recommendations

Risk Levels:

🟢 Low
🟡 Moderate
🟠 High
🔴 Critical

Installation
pip install -r requirements.txt
Run the Project
streamlit run app.py
Future Improvements
Multi-disease prediction
Doctor dashboard integration
Mobile application
Cloud deployment

Disclaimer
This project is designed as a decision-support and preventive screening tool. It should not be used as a replacement for professional medical advice.


