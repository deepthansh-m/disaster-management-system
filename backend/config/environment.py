import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:deepthanshm%Dimpu%402004@localhost/disaster_prediction")
API_KEY = os.getenv("OPENWEATHER_API_KEY", "Your api key")