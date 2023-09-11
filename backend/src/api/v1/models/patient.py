from api.v1.utils.database import db
from api.v1.models.base_model import BaseModel


class Patient(BaseModel, db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
