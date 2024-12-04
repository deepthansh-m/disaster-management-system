from flask import Blueprint, jsonify, request
from backend.database import get_db
from backend.models import DisasterHistory
from sqlalchemy.exc import SQLAlchemyError

disaster_bp = Blueprint('disaster', __name__, url_prefix='/api/disasters')

@disaster_bp.route('/', methods=['GET'])
def get_disasters():
    """Fetch all disaster records."""
    try:
        db = next(get_db())
        disasters = db.query(DisasterHistory).all()
        return jsonify([disaster.to_dict() for disaster in disasters]), 200
    except SQLAlchemyError as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@disaster_bp.route('/', methods=['POST'])
def add_disaster():
    """Add a new disaster record."""
    try:
        data = request.json
        db = next(get_db())
        disaster = DisasterHistory(
            location=data['location'],
            year=data['year'],
            disaster_type=data['disaster_type'],
            severity=data['severity']
        )
        db.add(disaster)
        db.commit()
        return jsonify({"status": "success", "message": "Disaster record added"}), 201
    except KeyError:
        return jsonify({"status": "error", "message": "Invalid data format"}), 400
    except SQLAlchemyError as e:
        return jsonify({"status": "error", "message": str(e)}), 500
