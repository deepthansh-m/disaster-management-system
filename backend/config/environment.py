import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Mani%402003@localhost/disaster_prediction")
API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
