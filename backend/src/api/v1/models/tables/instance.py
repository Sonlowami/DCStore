from api.v1.utils.database import db
from api.v1.models.tables.base_model import BaseModel


class Instance(BaseModel, db.Model):
    __tablename__ = 'instances'

    instanceNumber = db.Column(db.String(50))
    sopInstanceUID = db.Column(db.String(255))
    physicianName = db.Column(db.String(255))
    imageType = db.Column(db.JSON)  # Use a JSON field to store a list of strings
    series_id = db.Column(db.String(255), db.ForeignKey('series.id'), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)

    users = db.relationship('User', secondary='user_instance', viewonly=False)

    @staticmethod
    def extract_instance_metadata_from_file(file):
        """Extract instance metadata from a File instance and return a dictionary."""
        return {
            "instanceNumber": file.metadata.get('instanceNumber'),
            "sopInstanceUID": file.metadata.get('sopInstanceUID'),
            "physicianName": file.metadata.get('physicianName'),
            "imageType": file.metadata.get('imageType')
        }
    
    @staticmethod
    def get_instance_by_sopInstanceUID(sopInstanceUID):
        """Get an instance by sopInstanceUID"""
        return Instance.query.filter_by(sopInstanceUID=sopInstanceUID).first()
