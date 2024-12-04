import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Base configuration with default settings.
    """
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    DEBUG = False
    TESTING = False
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/disaster_management")

class DevelopmentConfig(Config):
    """
    Configuration for the development environment.
    """
    DEBUG = True
    DATABASE_URL = os.getenv("DEV_DATABASE_URL", Config.DATABASE_URL)

class TestingConfig(Config):
    """
    Configuration for the testing environment.
    """
    TESTING = True
    DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test_disaster_management.db")

class ProductionConfig(Config):
    """
    Configuration for the production environment.
    """
    DATABASE_URL = os.getenv("PROD_DATABASE_URL", Config.DATABASE_URL)

def get_config():
    """
    Returns the appropriate configuration class based on the environment.
    """
    env = os.getenv("FLASK_ENV", "development").lower()
    if env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()
