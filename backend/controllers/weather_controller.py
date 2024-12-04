import requests
from datetime import datetime
import time

API_KEY = 'your_openweather_api_key_here'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'
HISTORICAL_URL = 'http://api.openweathermap.org/data/2.5/onecall/timemachine'
GEOCODE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Function to fetch current weather data from OpenWeather API
def get_weather_data(location, historical=False, year=None):
    try:
        # Get the latitude and longitude for the location using OpenWeather's Geocoding API
        geocode_params = {
            'q': location,
            'appid': API_KEY
        }
        geocode_response = requests.get(GEOCODE_URL, params=geocode_params)
        location_data = geocode_response.json()

        if 'coord' not in location_data:
            print(f"Error: Unable to find location '{location}'")
            return None

        lat = location_data['coord']['lat']
        lon = location_data['coord']['lon']

        if historical:
            if not year:
                print("Error: Please provide a year for historical data.")
                return None

            # Calculate the timestamp for the target year (for example, for Jan 1st of that year)
            target_date = f"{year}-01-01 00:00:00"
            timestamp = int(time.mktime(datetime.strptime(target_date, "%Y-%m-%d %H:%M:%S").timetuple()))

            # Fetch historical weather data for a specific timestamp
            historical_url = f"{HISTORICAL_URL}?lat={lat}&lon={lon}&dt={timestamp}&appid={API_KEY}"
            response = requests.get(historical_url)
            return response.json()

        else:
            # Fetch current weather data for the given location
            params = {
                'q': location,
                'appid': API_KEY,
                'units': 'metric'
            }
            response = requests.get(BASE_URL, params=params)
            return response.json()

    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None
