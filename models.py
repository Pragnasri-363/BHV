from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db=SQLAlchemy()

class Notification(db.Model):
    __tablename__="notifications"
    id=db.Column(db.Integer,primary_key=True)
    #This serves as index to retrieve the required data
    patient_name=db.Column(db.String(100), nullable=False, index=True)
    image_name = db.Column(db.String(255), nullable=False)

    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    seen = db.Column(db.Boolean, default=False, index=True)

    def to_dict(self):
        """Convert notification to dictionary for JSON response"""
        return {
            "id": self.id,
            "patient_name": self.patient_name,
            "image_name": self.image_name,
            "title": self.title,
            "message": self.message,
            "seen": self.seen,
            "created_at": self.created_at.isoformat()
        }


