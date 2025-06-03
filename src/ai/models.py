from typing import Dict
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib   # type: ignore
from src.data_ingestion import get_order_book_metrics


class AIModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False

    def train(self, X_train: pd.DataFrame,
              y_train: pd.Series) -> None:  # type: ignore
        """Trains the AI Model"""
        print("Training AI model...")
        X_scaled = self.scaler.fit_transform(X_train)  # type: ignore
        self.model.fit(X_scaled, y_train)  # type: ignore[arg-type]
        self.is_trained = True  # Model is now trained
        print("AI model training complete.")

    def predict(self, feat: Dict[str, float],
                symbol: str = 'BTCUSDT') -> int:
        """
        Makes a prediction based on input features
        and order book analytics."""
        if not self.is_trained:
            raise Exception("Model is not trained yet.  \
                Please train the model before prediction.")
        # Optionally enrich features with order book metrics
        ob_mets = get_order_book_metrics(symbol)
        feat = {
            **feat,
            'ob_spread': (ob_mets['spread'] or 0.0),
            'ob_imbalance': (ob_mets['imbalance'] or 0.0)
        }
        X = pd.DataFrame([feat])
        X_scaled = self.scaler.transform(X)  # type: ignore
        prediction = self.model.predict(X_scaled)  # type: ignore
        return int(prediction[0])  # Return the single prediction

    def save_model(self, path: str = 'ai_model.joblib') -> None:
        """Save the trained model."""
        joblib.dump({'model': self.model,  # type: ignore
                     'scaler': self.scaler}, path)
        print(f"AI model saved to {path}")  # Model saved

    def load_model(self, path: str = 'ai_model.joblib') -> None:
        """Loads a pre-trained model."""
        try:
            data = joblib.load(path)  # type: ignore[no-untyped-call]
            self.model = data['model']
            self.scaler = data['scaler']
            self.is_trained = True
            print(f"AI model loaded from {path}")  # Model loaded
        except Exception:
            self.is_trained = False
            print(f"No model found at {path}. \
                  A new model will be used/trained.")  # No model found


if __name__ == "__main__":
    # Example: Simple dummy data for demonstration
    # Features: price_change (e.g., % change), volume_change
    # Target: 'buy' (1) or 'sell' (0)
    data = {  # type: ignore
        'price_change': [0.01, -0.005, 0.02, -0.01,
                         0.008, 0.03, -0.015, 0.002],
        'volume_change': [0.1, -0.05, 0.2, -0.1, 0.08, 0.3, -0.15, 0.02],
        'signal': [1, 0, 1, 0, 1, 1, 0, 1]  # 1 for buy, 0 for sell/hold
    }
    df = pd.DataFrame(data)

    X = df[['price_change', 'volume_change']]
    y = df['signal'].astype(int)

    ai_model = AIModel()
    ai_model.train(X, y)  # type: ignore

    # Make a prediction
    sample_features = {'price_change': 0.007, 'volume_change': 0.07}
    prediction = ai_model.predict(sample_features)
    print(f"Prediction for features {sample_features}: \
          {'Buy' if prediction == 1 else 'Sell/Hold'}")  # Print prediction

    ai_model.save_model()
