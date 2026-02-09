import os
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(PROJECT_ROOT, "DATA", "diabetes_dataset.csv")

def test_dataset_loads():
    assert os.path.exists(DATA_PATH), f"Dataset not found at {DATA_PATH}"
    df = pd.read_csv(DATA_PATH)
    assert not df.empty

def test_required_columns_exist():
    df = pd.read_csv(DATA_PATH)

    expected_columns = {
        "age",
        "bmi",
        "HbA1c_level",
        "blood_glucose_level",
        "hypertension",
        "heart_disease",
        "smoking_history",
        "diabetes"
    }

    assert expected_columns.issubset(df.columns)
