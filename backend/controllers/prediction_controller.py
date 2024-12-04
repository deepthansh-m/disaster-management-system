from flask import Blueprint, request, jsonify
from backend.ml.model_trainer import DisasterPredictor
from backend.utils.data_processor import process_prediction_data
from backend.database import get_db
from backend.models import DisasterHistory
from sqlalchemy.orm import Session

# Create a Blueprint for disaster prediction-related endpoints
prediction_bp = Blueprint('prediction', __name__, url_prefix='/api/predictions')

# Endpoint to predict disaster likelihood based on historical data and location
@prediction_bp.route('/predict', methods=['POST'])
def predict_disaster():
    data = request.json  # Get prediction data from the request body

    try:
        # Validate input data
        if 'location' not in data or 'year' not in data:
            return jsonify({"status": "error", "message": "Missing required fields: location and year"}), 400

        location = data['location']
        year = data['year']

        # Fetch historical data related to the location from the database
        db: Session = next(get_db())  # Get a database session
        disaster_history = db.query(DisasterHistory).filter(DisasterHistory.location.ilike(f"%{location}%")).all()

        # Check if we found any disaster history data
        if not disaster_history:
            return jsonify({"status": "error", "message": "No disaster history found for the provided location"}), 404

        # Process the disaster history data to prepare for prediction
        historical_data = [disaster.to_dict() for disaster in disaster_history]

        # Use DisasterPredictor to predict future disaster occurrence or severity
        predictor = DisasterPredictor(historical_data)
        prediction = predictor.predict(year)

        return jsonify({"status": "success", "prediction": prediction}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

# Endpoint to train the disaster prediction model
@prediction_bp.route('/train', methods=['POST'])
def train_model():
    data = request.json  # Get training data from the request body

    try:
        # Validate training data
        if 'location' not in data or 'years' not in data:
            return jsonify({"status": "error", "message": "Missing required fields: location and years"}), 400

        location = data['location']
        years = data['years']

        # Fetch historical data related to the location
        db: Session = next(get_db())  # Get a database session
        disaster_history = db.query(DisasterHistory).filter(DisasterHistory.location.ilike(f"%{location}%")).filter(DisasterHistory.year.in_(years)).all()

        if not disaster_history:
            return jsonify({"status": "error", "message": "No data found for the provided location and years"}), 404

        # Process the historical data for training
        historical_data = [disaster.to_dict() for disaster in disaster_history]

        # Train the disaster prediction model using the provided historical data
        model_trainer = DisasterPredictor(historical_data)
        model_trainer.train()

        # Save the trained model
        model_trainer.save_model()

        return jsonify({"status": "success", "message": "Model trained and saved successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()
