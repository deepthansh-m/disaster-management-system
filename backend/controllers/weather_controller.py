from flask import Blueprint, jsonify, request
from backend.services.openweather_service import get_weather_data
from flask_cors import CORS

weather_bp = Blueprint('weather', __name__, url_prefix='/api/weather')

@weather_bp.route('/current', methods=['GET'])
def current_weather():
    """Fetch current weather data for a location."""
    location = request.args.get('location')
    if not location:
        return jsonify({"status": "error", "message": "Location parameter is required"}), 400

    data = get_weather_data(location)
    if data:
        return jsonify(data), 200
    return jsonify({"status": "error", "message": "Failed to fetch weather data"}), 500
