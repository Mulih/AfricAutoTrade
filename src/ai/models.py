from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import joblib # For saving/loading models

class AIModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        # Will replace with training pipeline or pre-trained model

    def train(self, X_train, y_train):
        """Trains the AI Model"""
        print("Training AI model...")
        self.model.fit(X_train, y_train)
        print("AI model training complete.")

    def predict(self, features):
        """Makes a prediction based on input features."""
        # 'features' should be 2D array
        if isinstance(features, pd.Series):
            features = features.to_frame().T # convert Series to Dataframe and transpose
        elif isinstance(features, dict):
            features = pd.DataFrame([features])

        # Ensures features are in correct format for prediction
        # you might need to prepocess 'features' to match training data format
        # For this example, let's assume features are numeric.

        prediction = self.model.predict(features)
        return prediction[0] # return the single prediction

    def save_model(self, path="ai_model.joblib"):
        """Save the trained model."""
        joblib.dump(self.model, path)
        print(f"AI model saved to {path}")

    def load_model(self, path="ai_model.joblib"):
        """Loads a pre-trained model."""
        try:
            self.model = joblib.load(path)
            print(f"AI model loaded from {path}")
        except FileNotFoundError:
            print(F"No model found at {path}. A new model will be used/trained.")


if __main__ == "__main__":
    # Example: Simple dummy data for demonstration
    # Features: price_change (e.g., % change), volume_change
    # Target: 'buy' (1) or 'sell' (0)
    data = {
        'price_change': [0.01, -0.005, 0.02, -0.01, 0.008, 0.03, -0.015, 0.002],
        'volume_change': [0.1, -0.05, 0.2, -0.1, 0.08, 0.3, -0.15, 0.02],
        'signal': [1, 0, 1, 0, 1, 1, 0, 1] # 1 for buy, 0 for sell/hold
    }
    df = pd.DataFrame(data)

    X = df[['price_change', 'volume_change']]
    y = df['signal']

    ai_model = AIModel()
    ai_model.train(X, y)

    # Make a prediction
    sample_features = {'price_change': 0.007, 'volume_change': 0.07}
    prediction = ai_model.predict(sample_features)
    print(f"Prediction for features {sample_features}: {'Buy' if prediction == 1 else 'Sell/Hold'}")

    ai_model.save_model()