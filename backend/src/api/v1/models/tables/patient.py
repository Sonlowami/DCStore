from api.v1.utils.database import db
from api.v1.models.tables.base_model import BaseModel

from datetime import datetime


class Patient(BaseModel, db.Model):
    __tablename__ = 'patients'

    patientID = db.Column(db.String(255))
    patientName = db.Column(db.String(255))
    patientBirthDate = db.Column(db.Date)
    patientSex = db.Column(db.String(10))
    patientAge = db.Column(db.String(10))

    studies = db.relationship('Study', backref='patient', lazy=True)
    users = db.relationship('User', secondary='user_patient', viewonly=False)

    @staticmethod
    def extract_patient_metadata_from_file(file):
        """Extract patient metadata from a File instance and return a dictionary."""
        return {
            "patientID": file.metadata.get('patientID'),
            "patientName": file.metadata.get('patientName'),
            "patientBirthDate": file.metadata.get('patientBirthDate'),
            "patientSex": file.metadata.get('patientSex'),
            "patientAge": file.metadata.get('patientAge')
        }
    
    @staticmethod
    def get_patient_by_patientID(patientID):
        """Get a patient by patientID."""
        return Patient.query.filter_by(patientID=patientID).first()
