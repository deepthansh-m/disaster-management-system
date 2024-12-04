import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/disaster_db")
API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_openweather_api_key_here")
