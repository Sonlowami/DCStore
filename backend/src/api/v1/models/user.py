from api.v1.utils.database import db
from api.v1.models.base_model import BaseModel


class User(BaseModel, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(64), primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    files = db.relationship('File', backref='user', lazy=True)
