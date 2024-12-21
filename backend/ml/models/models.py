from backend.config.database import db
from datetime import datetime
from sqlalchemy import Enum

class DisasterHistory(db.Model):
    __tablename__ = 'disaster_history'

    id = db.Column(db.Integer, primary_key=True, index=True)
    disaster_type = db.Column(Enum('Earthquake', 'Flood', 'Cyclone', 'Drought', name='disaster_type_enum'), nullable=False)
    location = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String, nullable=True)

    # Existing columns
    latitude = db.Column(db.Float, nullable=False, index=True)
    longitude = db.Column(db.Float, nullable=False, index=True)
    rainfall = db.Column(db.Float, nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    disaster_occurred = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "disaster_type": self.disaster_type,
            "location": self.location,
            "date": self.date.strftime('%Y-%m-%d') if self.date else None,
            "description": self.description,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "rainfall": self.rainfall,
            "temperature": self.temperature,
            "disaster_occurred": self.disaster_occurred
        }
