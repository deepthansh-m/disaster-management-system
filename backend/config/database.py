# backend/config/database.py
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Flask-SQLAlchemy
db = SQLAlchemy()

def get_db():
    """Get database session."""
    return db.session