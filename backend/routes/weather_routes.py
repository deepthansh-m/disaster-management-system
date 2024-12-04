from flask import Blueprint, jsonify
from backend.services.openweather_service import get_weather_data

weather_bp = Blueprint('weather', __name__, url_prefix='/api/weather')

@weather_bp.route('/current', methods=['GET'])
def get_current_weather():
    location = request.args.get('location')
    try:
        if not location:
            return jsonify({"status": "error", "message": "Location is required"}), 400

        weather_data = get_weather_data(location)
        return jsonify({"status": "success", "data": weather_data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
