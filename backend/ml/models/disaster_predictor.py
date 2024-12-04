import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class DisasterPredictor:
    def __init__(self, model_path='ml_models/disaster_prediction_model.pkl'):
        self.model_path = model_path
        self.model = None

    def load_model(self):
        """Load the trained model from the file."""
        try:
            with open(self.model_path, 'rb') as file:
                self.model = pickle.load(file)
        except FileNotFoundError:
            self.model = RandomForestClassifier()

    def train(self, X, y):
        """Train the disaster prediction model."""
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        self.save_model()

    def predict(self, features):
        """Predict disasters based on input features."""
        if not self.model:
            self.load_model()
        features = np.array(features).reshape(1, -1)
        return self.model.predict(features)

    def save_model(self):
        """Save the trained model to the file."""
        with open(self.model_path, 'wb') as file:
            pickle.dump(self.model, file)
