import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer

def load_and_prepare_data(csv_path):
    df = pd.read_csv(csv_path)

    # Replace invalid strings
    df.replace(["No Info", "Unknown", "none"], pd.NA, inplace=True)

    # Encode categorical columns
    categorical_cols = ["gender", "smoking_history"]
    encoder = LabelEncoder()

    for col in categorical_cols:
        df[col] = encoder.fit_transform(df[col].astype(str))

    # Separate features and target
    X = df.drop("diabetes", axis=1)
    y = df["diabetes"]

    # Handle missing values
    imputer = SimpleImputer(strategy="median")
    X = imputer.fit_transform(X)

    return X, y
