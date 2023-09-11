from api.v1.utils.database import db
from api.v1.models.base_model import BaseModel
from api.v1.models.study import Study


class Series(BaseModel, db.Model):
    __tablename__ = 'series'

    id = db.Column(db.Integer, primary_key=True)
    study_id = db.Column(db.Integer, db.ForeignKey(Study.id), nullable=False)
    modality = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
