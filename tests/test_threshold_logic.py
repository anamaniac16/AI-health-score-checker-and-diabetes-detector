import json

def test_threshold_loaded():
    with open("models/diabetes_threshold.json") as f:
        threshold = json.load(f)["threshold"]

    assert 0.1 <= threshold <= 0.6
