from backend.config.database import db

class DisasterHistory(db.Model):
    __tablename__ = 'disaster_history'
    
    id = db.Column(db.Integer, primary_key=True, index=True)
    disaster_type = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String, nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "disaster_type": self.disaster_type,
            "location": self.location,
            "date": self.date.isoformat(),
            "description": self.description
        }