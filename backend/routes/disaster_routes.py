from flask import Blueprint, request, jsonify
from backend.controllers.disaster_controller import DisasterController

# Create a Blueprint for the disaster-related routes
disaster_routes = Blueprint('disaster_routes', __name__)

# Initialize the DisasterController
disaster_controller = DisasterController()


# Route to get disaster history for a specific location
@disaster_routes.route('/disaster/history', methods=['GET'])
def get_disaster_history():
    try:
        # Get the location name from query parameters
        location = request.args.get('location')

        if not location:
            return jsonify({"error": "Location parameter is required"}), 400

        # Fetch disaster history from the controller
        disaster_history = disaster_controller.get_disaster_history(location)

        if disaster_history:
            return jsonify(disaster_history), 200
        else:
            return jsonify({"message": "No disaster history found for this location"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to get the disaster prediction for a specific location
@disaster_routes.route('/disaster/predict', methods=['POST'])
def predict_disaster():
    try:
        # Get the location and other required data from the request body
        data = request.get_json()

        location = data.get('location')
        if not location:
            return jsonify({"error": "Location is required"}), 400

        # Get the disaster prediction from the controller
        prediction = disaster_controller.predict_disaster(location)

        if prediction:
            return jsonify(prediction), 200
        else:
            return jsonify({"message": "No prediction available for this location"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
