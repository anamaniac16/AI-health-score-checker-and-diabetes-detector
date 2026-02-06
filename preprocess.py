import pandas as pd

# Load dataset
df = pd.read_csv("DATA/Data.csv")



print("Dataset loaded successfully")
print(df.head())
print("\n📌 Column names:")
print(df.columns)

print("\n📌 Dataset info:")
print(df.info())
if "diabetes" in df.columns:
    df = df.drop("diabetes", axis=1)

print("\n✅ Removed disease column (risk-based system)")
print(df.head())
print("\n📌 Missing values check:")
print(df.isnull().sum())

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

df["gender"] = le.fit_transform(df["gender"])
df["smoking_history"] = le.fit_transform(df["smoking_history"])

print("\n✅ Encoded categorical columns")
print(df.head())
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

numeric_cols = [
    "age",
    "bmi",
    "HbA1c_level",
    "blood_glucose_level"
]

df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

print("\n✅ Scaled numeric values")
print(df.head())
