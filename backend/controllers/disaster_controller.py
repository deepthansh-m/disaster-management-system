from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import DisasterHistory
from backend.utils.data_processor import process_disaster_data

# Create a Blueprint for disaster-related endpoints
disaster_bp = Blueprint('disaster', __name__, url_prefix='/api/disasters')

# Fetch all disaster records or filter by location
@disaster_bp.route('/', methods=['GET'])
def get_disaster_history():
    location = request.args.get('location', None)
    db: Session = next(get_db())  # Get a database session

    try:
        if location:
            disasters = db.query(DisasterHistory).filter(DisasterHistory.location.ilike(f"%{location}%")).all()
        else:
            disasters = db.query(DisasterHistory).all()

        disaster_list = [
            {
                "id": disaster.id,
                "location": disaster.location,
                "disaster_type": disaster.disaster_type,
                "year": disaster.year,
                "severity": disaster.severity,
            }
            for disaster in disasters
        ]

        return jsonify({"status": "success", "data": disaster_list}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

# Add a new disaster record
@disaster_bp.route('/add', methods=['POST'])
def add_disaster():
    data = request.json
    db: Session = next(get_db())  # Get a database session

    try:
        new_disaster = DisasterHistory(
            location=data['location'],
            disaster_type=data['disaster_type'],
            year=data['year'],
            severity=data['severity']
        )
        db.add(new_disaster)
        db.commit()
        db.refresh(new_disaster)

        return jsonify({"status": "success", "data": {"id": new_disaster.id}}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

# Analyze disaster data
@disaster_bp.route('/analyze', methods=['POST'])
def analyze_disaster_data():
    data = request.json
    db: Session = next(get_db())  # Get a database session

    try:
        # Use a utility function to process disaster data
        analysis_result = process_disaster_data(data, db)

        return jsonify({"status": "success", "data": analysis_result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()
