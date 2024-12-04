import joblib
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load model from the file system
MODEL_PATH = os.getenv('DISASTER_MODEL_PATH')

class PredictionService:
    def __init__(self):
        # Ensure the model path is available
        if not MODEL_PATH:
            raise ValueError("Model path is missing. Please set DISASTER_MODEL_PATH in the .env file.")
        self.model = self.load_model()

    def load_model(self):
        """Loads the pre-trained machine learning model."""
        try:
            model = joblib.load(MODEL_PATH)
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            return None

    def predict_disaster(self, features):
        """Predict disaster likelihood based on input features."""
        try:
            if self.model:
                prediction = self.model.predict([features])
                return prediction[0]  # Return the first (and only) prediction
            else:
                raise Exception("Model is not loaded properly.")
        except Exception as e:
            print(f"Error in prediction: {e}")
            return None
