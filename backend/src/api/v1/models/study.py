from api.v1.utils.database import db
from api.v1.models.base_model import BaseModel
from api.v1.models.patient import Patient


class Study(BaseModel, db.Model):
    __tablename__ = 'studies'

    id = db.Column(db.String(64), primary_key=True)
    patient_id = db.Column(db.String(64), db.ForeignKey(Patient.id), nullable=False)
    date = db.Column(db.Date, nullable=False)
    physician = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    series = db.relationship('Series', backref='study', lazy=True)
