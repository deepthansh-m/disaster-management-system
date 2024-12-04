import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenWeather API key from environment variables
API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "https://api.openweathermap.org/data/2.5/"


class OpenWeatherService:
    def __init__(self):
        # Ensure the API key is available
        if not API_KEY:
            raise ValueError("API key is missing. Please set OPENWEATHER_API_KEY in the .env file.")

    def get_current_weather(self, location):
        """Fetch current weather data for a given location."""
        try:
            url = f"{BASE_URL}weather?q={location}&appid={API_KEY}&units=metric"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                current_weather = {
                    "location": location,
                    "temperature": f"{data['main']['temp']}°C",
                    "humidity": f"{data['main']['humidity']}%",
                    "conditions": data['weather'][0]['description'].capitalize(),
                    "wind_speed": f"{data['wind']['speed']} km/h"
                }
                return current_weather
            else:
                raise Exception(f"Error fetching weather data: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_weather_forecast(self, location):
        """Fetch weather forecast data for a given location."""
        try:
            url = f"{BASE_URL}forecast?q={location}&appid={API_KEY}&units=metric"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                forecast_data = []
                for forecast in data['list']:
                    forecast_data.append({
                        "date": forecast['dt_txt'],
                        "temperature": f"{forecast['main']['temp']}°C",
                        "conditions": forecast['weather'][0]['description'].capitalize(),
                        "precipitation": f"{forecast['pop'] * 100}%"  # Probability of precipitation
                    })
                return forecast_data
            else:
                raise Exception(f"Error fetching forecast data: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error: {e}")
            return None
