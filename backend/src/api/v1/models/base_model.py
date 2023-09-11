from api.v1.utils.database import db

from datetime import datetime
import uuid


class BaseModel(db.Model):
    """BaseModel class"""
    __abstract__ = True

    record_id = db.Column(db.String(60), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize BaseModel"""
        self.record_id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

    def save(self):
        """Save BaseModel"""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete BaseModel"""
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """Return dictionary of BaseModel"""
        dict = {}
        for key, value in self.__dict__.items():
            if key == "_sa_instance_state":
                continue
            if isinstance(value, datetime):
                dict[key] = value.strftime('%Y-%m-%dT%H:%M:%S.%f')
            else:
                dict[key] = value
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict
    
    def __str__(self):
        """Return string representation of BaseModel"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.record_id, self.__dict__)
