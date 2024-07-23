from sklearn.ensemble import IsolationForest
import pandas as pd

class Predictor:
    def __init__(self):
        self.model = IsolationForest()

    def fit(self, data):
        # Prepare data for fitting
        if 'timestamp' in data.columns:
            data = data.drop(columns=['timestamp'])
        if data.empty:
            raise ValueError("Training data is empty.")
        self.model.fit(data)

    def predict(self, data):
        # Prepare data for prediction
        if 'timestamp' in data.columns:
            data = data.drop(columns=['timestamp'])
        if data.empty:
            raise ValueError("Prediction data is empty.")
        return self.model.predict(data)
