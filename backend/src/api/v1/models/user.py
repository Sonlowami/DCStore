from jsonschema import validate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from api.v1.utils.database import mongo


class User:
    """User class for mongodb"""

    def __init__(self, *args, **kwargs):
        """Initialize User class"""
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.username = kwargs.get('username')
        self.fullname = kwargs.get('fullname')
        self.role = kwargs.get('role')
        self.patients = {}
        self.files = []
        self.verify_schema()

    def verify_schema(self):
        """Verify user schema"""
        USER_SCHEMA = {
            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "password": {"type": "string"},
                "username": {"type": "string"},
                "fullname": {"type": "string"},
                "role": {"type": "string"},
                "files": {"type": "array"},
                "patients": {"type": "object"},
            },
            "required": ["email", "password", "username", "fullname", "role", "patients", "files"]
        }
        # Validate user schema
        validate(instance=self.__dict__, schema=USER_SCHEMA)

    def save(self):
        """Save user to mongodb"""
        user = {
            "email": self.email,
            "password_hash": generate_password_hash(self.password), # type: ignore
            "username": self.username,
            "fullname": self.fullname,
            "role": self.role,
            "files": self.files,
            "patients": self.patients,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        return mongo.db.users.insert_one(user) # type: ignore
    
    def update(self, update_query):
        """Update user in mongodb"""
        return mongo.db.users.update_one({"email": self.email}, update_query)

    @staticmethod
    def get_user(email):
        """Get user from mongodb"""
        user = mongo.db.users.find_one({"email": email}) # type: ignore
        return user

    @staticmethod
    def get_user_by_id(id):
        """Get user from mongodb"""
        user = mongo.db.users.find_one({"_id": id}) # type: ignore
        return user
    
    @staticmethod
    def get_user_by_username(username):
        """Get user from mongodb"""
        user = mongo.db.users.find_one({"username": username}) # type: ignore
        return user
