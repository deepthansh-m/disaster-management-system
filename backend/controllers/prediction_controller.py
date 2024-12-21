from flask import Blueprint, request, jsonify
from backend.ml.models.disaster_predictor import DisasterPredictor
from backend.config.database import get_db
from backend.ml.models.models import DisasterHistory
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

prediction_bp = Blueprint('prediction', __name__, url_prefix='/api/predictions')

@prediction_bp.route('/', methods=['POST'], strict_slashes=False)
def predict_disaster():
    logging.info("Received prediction request")
    try:
        data = request.get_json()
        if not data:
            logging.warning("No data provided in request")
            return jsonify({"error": "No data provided"}), 400

        coordinates = data.get('coordinates')
        location = data.get('location', 'Unknown')

        # Extract specific parameters or use defaults
        rainfall = data.get('rainfall', 0.8)
        temperature = data.get('temperature', 23.0)

        if not coordinates:
            logging.warning("Coordinates are missing in the request")
            return jsonify({"error": "Coordinates are required"}), 400

        latitude = coordinates.get('latitude')
        longitude = coordinates.get('longitude')

        if latitude is None or longitude is None:
            logging.warning("Latitude or longitude is missing")
            return jsonify({"error": "Latitude and longitude are required"}), 400

        # Initialize your DisasterPredictor and get predictions
        predictor = DisasterPredictor()
        prediction_result = predictor.predict(
            latitude=latitude,
            longitude=longitude,
            region=location,
            parameters={
                'rainfall': rainfall,
                'temperature': temperature
            }
        )

        # Store prediction in the database
        try:
            db_session = get_db()

            # Create DisasterHistory instance
            disaster_history = DisasterHistory(
                disaster_type=prediction_result.get('result', 'Unknown'),
                location=location,
                latitude=latitude,
                longitude=longitude,
                rainfall=rainfall,
                temperature=temperature,
                date=datetime.utcnow().date(),
                description=f"Prediction confidence: {prediction_result.get('confidence', 0.0)}",
                disaster_occurred=prediction_result.get('confidence', 0.0) > 0.5
            )

            db_session.add(disaster_history)
            db_session.commit()
            logging.info("Prediction stored in the database successfully")
        except SQLAlchemyError as e:
            db_session.rollback()
            logging.error(f"Database error occurred: {str(e)}")
            return jsonify({"error": f"Database error: {str(e)}"}), 500

        logging.info("Prediction successfully processed")
        return jsonify(prediction_result), 200

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500
