from flask import Blueprint, request, jsonify
from backend.controllers.weather_controller import WeatherController

# Create a Blueprint for the weather-related routes
weather_routes = Blueprint('weather_routes', __name__)

# Initialize the WeatherController
weather_controller = WeatherController()


# Route to get current weather data for a location
@weather_routes.route('/weather/current', methods=['GET'])
def get_current_weather():
    try:
        # Get location from query parameters
        location = request.args.get('location')

        if not location:
            return jsonify({"error": "Location is required"}), 400

        # Get the current weather for the location from the controller
        weather_data = weather_controller.get_current_weather(location)

        if weather_data:
            return jsonify(weather_data), 200
        else:
            return jsonify({"message": "Weather data not available for this location"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to get weather forecast data for a location
@weather_routes.route('/weather/forecast', methods=['GET'])
def get_weather_forecast():
    try:
        # Get location from query parameters
        location = request.args.get('location')

        if not location:
            return jsonify({"error": "Location is required"}), 400

        # Get the weather forecast for the location from the controller
        forecast_data = weather_controller.get_weather_forecast(location)

        if forecast_data:
            return jsonify(forecast_data), 200
        else:
            return jsonify({"message": "Weather forecast not available for this location"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
