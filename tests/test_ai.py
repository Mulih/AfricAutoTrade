from src.ai.models import AIModel
import pandas as pd


def test_ai_model_train_and_predict():
    data = {  # type: ignore
        'price_change': [0.01, -0.005, 0.02, -0.01],
        'volume_change': [0.1, -0.05, 0.2, -0.1],
        'signal': [1, 0, 1, 0]
    }
    df = pd.DataFrame(data)
    X = df[['price_change', 'volume_change']]
    y = df['signal']  # type: ignore
    model = AIModel()
    model.train(X, y)  # type: ignore
    assert model.is_trained
    pred = model.predict({'price_change': 0.01, 'volume_change': 0.1})
    assert pred in [0, 1]
