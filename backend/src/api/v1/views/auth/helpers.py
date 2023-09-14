from flask import jsonify

from api.v1.models.user import User
from api.v1.utils.database import db

def getuser(email: str) -> User:
    """Check if a given email is of a valid user in the database and
    return that user"""
    try:
        user: User = db.session.query(User).filter_by(email=email).first()
        return user
    except Exception as e:
        print(e)
