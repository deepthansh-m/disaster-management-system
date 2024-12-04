import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from backend.ml.models.model_trainer import train_disaster_model


class DisasterPredictor:
    def __init__(self):
        # Load the trained model and scaler from disk
        self.model = None
        self.scaler = None
        self.load_model()

    def load_model(self):
        """
        Loads the trained disaster prediction model and scaler from files.
        """
        try:
            # Load model
            with open('backend/ml/models/disaster_prediction_model.pkl', 'rb') as f:
                self.model = pickle.load(f)

            # Load scaler
            with open('backend/ml/models/scaler.pkl', 'rb') as f:
                self.scaler = pickle.load(f)

            print("Model and Scaler loaded successfully.")
        except Exception as e:
            print(f"Error loading model or scaler: {str(e)}")

    def predict_disaster(self, location_data):
        """
        Predicts the likelihood of a disaster for the given location data.
        :param location_data: Dictionary containing location data (e.g., temperature, humidity, etc.)
        :return: Prediction result
        """
        try:
            # Prepare input data for prediction
            features = np.array([
                location_data['temperature'],
                location_data['humidity'],
                location_data['rainfall'],
                location_data['wind_speed']
            ])

            # Scale the input features using the same scaler as the training phase
            features_scaled = self.scaler.transform([features])

            # Make prediction using the model
            prediction = self.model.predict(features_scaled)

            # Return prediction (0: No disaster, 1: Disaster predicted)
            return prediction[0]

        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            return None

    def get_disaster_history(self, location_name):
        """
        Fetches historical disaster data for the given location.
        :param location_name: Name of the location
        :return: List of disaster events for the location
        """
        # This is a placeholder function. You can replace it with actual database queries.
        disaster_history = [
            {"date": "2021-06-15", "type": "Flood", "severity": "High"},
            {"date": "2022-03-10", "type": "Earthquake", "severity": "Medium"},
            {"date": "2023-07-25", "type": "Wildfire", "severity": "High"}
        ]
        return disaster_history

    def predict_disaster_for_location(self, location_name):
        """
        Predicts disaster for a location using both historical data and model prediction.
        :param location_name: Name of the location
        :return: Prediction and disaster history
        """
        # First, get historical disaster data for the location
        disaster_history = self.get_disaster_history(location_name)

        # Get some data to pass to the model (use a mock-up for now)
        location_data = {
            'temperature': 30.0,  # Example data
            'humidity': 75.0,
            'rainfall': 10.0,
            'wind_speed': 15.0
        }

        # Get model prediction
        prediction = self.predict_disaster(location_data)

        # Return both prediction and history
        return {
            "location_name": location_name,
            "disaster_history": disaster_history,
            "disaster_prediction": "Disaster predicted" if prediction == 1 else "No disaster predicted"
        }
