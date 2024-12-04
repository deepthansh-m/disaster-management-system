from flask import Blueprint, request, jsonify
from backend.controllers.prediction_controller import PredictionController

# Create a Blueprint for the prediction-related routes
prediction_routes = Blueprint('prediction_routes', __name__)

# Initialize the PredictionController
prediction_controller = PredictionController()


# Route to get the prediction model
@prediction_routes.route('/predict/model', methods=['GET'])
def get_prediction_model():
    try:
        # Fetch the prediction model from the controller
        model = prediction_controller.get_model()

        if model:
            return jsonify({"message": "Prediction model loaded successfully"}), 200
        else:
            return jsonify({"error": "Prediction model could not be loaded"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to make a disaster prediction based on location
@prediction_routes.route('/predict', methods=['POST'])
def make_prediction():
    try:
        # Get location and disaster parameters from request body
        data = request.get_json()
        location = data.get('location')

        if not location:
            return jsonify({"error": "Location is required"}), 400

        # Get the disaster prediction from the controller
        prediction = prediction_controller.predict_disaster(location)

        if prediction:
            return jsonify(prediction), 200
        else:
            return jsonify({"message": "No prediction available for this location"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
