from api.v1.utils.database import db
from api.v1.models.tables.base_model import BaseModel

class Series(BaseModel, db.Model):
    __tablename__ = 'series'

    seriesDescription = db.Column(db.String(255))
    seriesInstanceUID = db.Column(db.String(255))
    seriesNumber = db.Column(db.String(50))
    modality = db.Column(db.String(50))
    studyID = db.Column(db.String(255), db.ForeignKey('studies.id'), nullable=False)
    instances = db.relationship('Instance', backref='series', lazy=True)

    users = db.relationship('User', secondary='user_series', viewonly=False)

    @staticmethod
    def extract_series_metadata_from_file(file):
        """Extract series metadata from a File instance and return a dictionary."""
        return {
            "seriesDescription": file.metadata.get('seriesDescription'),
            "seriesInstanceUID": file.metadata.get('seriesInstanceUID'),
            "seriesNumber": file.metadata.get('seriesNumber'),
            "modality": file.metadata.get('modality')
        }
    
    @staticmethod
    def get_series_by_seriesInstanceUID(seriesInstanceUID):
        """Get series by seriesInstanceUID"""
        return Series.query.filter_by(seriesInstanceUID=seriesInstanceUID).first()
