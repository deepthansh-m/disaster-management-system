from flask import Blueprint, request, jsonify
from backend.ml.models.disaster_predictor import DisasterPredictor
from backend.config import get_db
from backend.ml.models import DisasterHistory
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS

prediction_bp = Blueprint('prediction', __name__, url_prefix='/api/predictions/')

@prediction_bp.route('/predict', methods=['POST'])
def predict_disaster():
    """Predict disaster likelihood."""
    data = request.json
    try:
        db_session = get_db()
        # Rest of the code...
        location = data.get('location')
        year = data.get('year')

        if not location or not year:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        db = next(get_db())
        historical_data = db.query(DisasterHistory).filter(
            DisasterHistory.location.ilike(f"%{location}%")
        ).all()

        if not historical_data:
            return jsonify({"status": "error", "message": "No historical data found"}), 404

        features = [disaster.to_dict() for disaster in historical_data]
        predictor = DisasterPredictor()
        predictor.load_model()
        prediction = predictor.predict([features])

        return jsonify({"status": "success", "prediction": prediction.tolist()}), 200
    except SQLAlchemyError as e:
        return jsonify({"status": "error", "message": str(e)}), 500
