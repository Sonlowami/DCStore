from api.v1.utils.database import db
from api.v1.models.tables.base_model import BaseModel, time

from datetime import datetime


class Study(BaseModel, db.Model):
    __tablename__ = 'studies'

    studyDescription = db.Column(db.String(255))
    studyDate = db.Column(db.Date)
    studyInstanceUID = db.Column(db.String(255))
    patient_id = db.Column(db.String(255), db.ForeignKey('patients.id'), nullable=False)
    series = db.relationship('Series', backref='study', lazy=True)

    users = db.relationship('User', secondary='user_study', viewonly=False)

    @staticmethod
    def extract_study_metadata_from_file(file):
        """Extract study metadata from a File instance and return a dictionary."""
        return {
            "studyDescription": file.metadata.get('studyDescription'),
            "studyDate": file.metadata.get('studyDate'),
            "studyInstanceUID": file.metadata.get('studyInstanceUID')
        }
    
    @staticmethod
    def get_study_by_studyInstanceUID(studyInstanceUID):
        """Get a study by studyInstanceUID"""
        return Study.query.filter_by(studyInstanceUID=studyInstanceUID).first()
