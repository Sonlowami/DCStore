from api.v1.utils.database import db

from uuid import uuid4
from datetime import datetime


time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """Base data model for all objects"""

    id = db.Column(db.String(80), primary_key=True, default=lambda: str(uuid4()))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        """Define a base way to print models"""
        return f"{self.__class__.__name__} <{self.id}>"

    def save(self):
        """Save an object to the database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def delete(self):
        """Delete an object from the database"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
