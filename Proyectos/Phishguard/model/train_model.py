"""
Train and save a RandomForest model to detect phishing URLs.
"""
import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def train_and_export(data_path: str, output_dir: str):
    # Load dataset
    data = pd.read_csv(data_path)
    # Separate features and labels
    X = data.drop(columns=["label"])
    y = data["label"]

    # Split into train/test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Initialize and train classifier
    classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    classifier.fit(X_train, y_train)

    # Evaluate performance
    predictions = classifier.predict(X_test)
    accuracy = accuracy_score(y_test, predictions) * 100
    print(f"Model accuracy: {accuracy:.2f}%")

    # Ensure model directory exists
    os.makedirs(output_dir, exist_ok=True)
    model_file = os.path.join(output_dir, "phishing_model.pkl")
    joblib.dump(classifier, model_file)
    print(f"Trained model saved to {model_file}")

if __name__ == "__main__":
    train_and_export(
        data_path=os.path.join("data", "urls.csv"),
        output_dir=os.path.join("model")
    )
