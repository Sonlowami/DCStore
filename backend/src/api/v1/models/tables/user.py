from werkzeug.security import generate_password_hash

from api.v1.utils.database import db
from api.v1.models.tables.base_model import BaseModel
from api.v1.models.tables.many_to_many import user_patient, user_study, user_series, user_instance

from datetime import datetime


class User(BaseModel, db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(240), nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)

    patients = db.relationship('Patient', secondary=user_patient, overlaps='users')
    studies = db.relationship('Study', secondary=user_study, overlaps='users')
    series = db.relationship('Series', secondary=user_series, overlaps='users')
    instances = db.relationship('Instance', secondary=user_instance, overlaps='users')

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if key == 'password':
                key = 'password_hash'
                value = generate_password_hash(value)
            setattr(self, key, value)

    def __repr__(self):
        return '<User %r>' % self.name
    
    def update_user(self, **kwargs):
        new_username = kwargs.get('username')
        if new_username:
            if User.get_user_by_username(new_username):
                raise Exception('Username already exists')
            self.username = new_username
        new_email = kwargs.get('email')
        if new_email:
            if User.get_user(new_email):
                raise Exception('Email already exists')
            self.email = new_email
        new_password = kwargs.get('password')
        if new_password:
            self.password_hash = generate_password_hash(new_password)
        new_fullname = kwargs.get('fullname')
        if new_fullname:
            self.fullname = new_fullname
        new_role = kwargs.get('role')
        if new_role:
            self.role = new_role
        self.updated_at = datetime.now()
        self.save()

    
    @staticmethod
    def get_user(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()
