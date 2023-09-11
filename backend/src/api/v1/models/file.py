from api.v1.utils.database import db
from api.v1.models.base_model import BaseModel
from api.v1.models.instance import Instance
from api.v1.models.user import User


class File(BaseModel, db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    instance_id = db.Column(db.Integer, db.ForeignKey(Instance.id), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    md5 = db.Column(db.String(32), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
