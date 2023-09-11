from api.v1.utils.database import db
from api.v1.models.base_model import BaseModel
from api.v1.models.series import Series


class Instance(BaseModel, db.Model):
    __tablename__ = 'instances'

    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey(Series.id), nullable=False)
    content_datetime = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(255), nullable=False)
