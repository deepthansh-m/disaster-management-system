import joblib
import numpy as np
import pandas as pd
import logging
from sklearn.ensemble import RandomForestClassifier

# Configure logging
logging.basicConfig(level=logging.INFO)


class DisasterPredictor:
    def __init__(self):
        """Initialize the DisasterPredictor with a trained model."""
        model_path = 'backend/ml/models/trained/disaster_model.pkl'
        scaler_path = 'backend/ml/models/trained/scaler.pkl'
        encoder_path = 'backend/ml/models/trained/label_encoder.pkl'

        # Define valid disaster types that match your database enum
        self.valid_disaster_types = ['Earthquake', 'Flood', 'Cyclone', 'Drought']

        try:
            self.model = self.load_model(model_path)
            logging.info("Model loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load model: {e}")
            self.model = RandomForestClassifier()

        try:
            self.scaler = self.load_model(scaler_path)
            logging.info("Scaler loaded successfully.")
        except Exception as e:
            logging.warning(f"Failed to load scaler: {e}")
            self.scaler = None

        try:
            self.label_encoder = self.load_model(encoder_path)
            # Ensure label encoder knows about all possible classes
            self.label_encoder.classes_ = np.array(self.valid_disaster_types)
            logging.info("Label encoder loaded successfully.")
        except Exception as e:
            logging.warning(f"Failed to load label encoder: {e}")
            self.label_encoder = None

    def load_model(self, model_path):
        """Load a trained model from disk."""
        try:
            model = joblib.load(model_path)
            return model
        except Exception as e:
            logging.error(f"Failed to load model from {model_path}: {e}")
            raise

    def predict(self, latitude, longitude, region=None, parameters=None):
        """
        Make prediction using the loaded model.

        Args:
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            region (str, optional): Geographic region
            parameters (dict, optional): Additional parameters like rainfall and temperature

        Returns:
            dict: Prediction result and confidence score
        """
        try:
            # Log inputs
            logging.info(f"Predicting for latitude: {latitude}, longitude: {longitude}")
            logging.info(f"Region: {region}, Parameters: {parameters}")

            # Validate inputs
            if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
                raise ValueError("Latitude and longitude must be numeric values")

            # Default values for missing parameters
            parameters = parameters or {}
            rainfall = float(parameters.get('rainfall', 0.8))
            temperature = float(parameters.get('temperature', 23.0))

            # Prepare feature vector
            features = pd.DataFrame([[
                latitude,
                longitude,
                rainfall,
                temperature
            ]], columns=['latitude', 'longitude', 'rainfall', 'temperature'])

            # Scale features if scaler exists
            if self.scaler:
                features = self.scaler.transform(features)
            else:
                logging.warning("No scaler found, skipping scaling.")

            # Make prediction
            prediction = self.model.predict(features)[0]
            confidence = float(self.model.predict_proba(features)[0].max())

            # Handle prediction decoding
            try:
                if isinstance(prediction, (int, np.integer)):
                    # Ensure prediction index is within bounds
                    if 0 <= prediction < len(self.valid_disaster_types):
                        result = self.valid_disaster_types[prediction]
                    else:
                        logging.warning(f"Prediction index {prediction} out of bounds")
                        result = self.valid_disaster_types[0]  # Default to first disaster type
                else:
                    # If prediction is already a string, validate it
                    result = str(prediction)
                    if result not in self.valid_disaster_types:
                        result = self.valid_disaster_types[0]  # Default to first disaster type

                logging.info(f"Successfully decoded prediction to: {result}")
            except Exception as e:
                logging.error(f"Error in prediction decoding: {e}")
                result = self.valid_disaster_types[0]  # Default to first disaster type

            return {
                "result": result,
                "confidence": confidence,
                "region": region,
                "parameters": parameters
            }

        except Exception as e:
            logging.error(f"Unexpected prediction error: {e}")
            return {
                "result": self.valid_disaster_types[0],  # Default to first disaster type
                "confidence": 0.0,
                "error": str(e)
            }