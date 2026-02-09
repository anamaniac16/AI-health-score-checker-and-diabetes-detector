from models.ml_diabetes_predict import predict_diabetes

def test_high_risk_patient():
    user_data = {
        "age": 65,
        "bmi": 34,
        "HbA1c_level": 7.2,
        "blood_glucose_level": 180,
        "hypertension": 1,
        "heart_disease": 1,
        "smoking_history": 2
    }

    pred, prob, _, _ = predict_diabetes(user_data)


    assert pred == 1
    assert prob > 70
