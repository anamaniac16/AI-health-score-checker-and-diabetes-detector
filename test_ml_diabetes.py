import unittest
from models.ml_diabetes_predict import predict_diabetes

class TestDiabetesPrediction(unittest.TestCase):

    def setUp(self):
        # Valid baseline input
        self.valid_input = {
            "age": 45,
            "bmi": 27.5,
            "HbA1c_level": 6.2,
            "blood_glucose_level": 140,
            "hypertension": 1,
            "heart_disease": 0,
            "smoking_history": 1
        }

    def test_prediction_runs(self):
        pred, prob, shap, warnings = predict_diabetes(self.valid_input)
        self.assertIn(pred, [0, 1])

    def test_probability_range(self):
        _, prob, _, _ = predict_diabetes(self.valid_input)
        self.assertGreaterEqual(prob, 0)
        self.assertLessEqual(prob, 100)

    def test_shap_output(self):
        _, _, shap, _ = predict_diabetes(self.valid_input)
        self.assertIsInstance(shap, dict)
        self.assertGreater(len(shap), 0)

    def test_extreme_values(self):
        extreme_input = {
            "age": 90,
            "bmi": 45,
            "HbA1c_level": 12,
            "blood_glucose_level": 350,
            "hypertension": 1,
            "heart_disease": 1,
            "smoking_history": 2
        }
        pred, _, _, _ = predict_diabetes(extreme_input)
        self.assertEqual(pred, 1)

if __name__ == "__main__":
    unittest.main()
