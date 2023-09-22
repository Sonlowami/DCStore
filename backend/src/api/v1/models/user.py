from jsonschema import validate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from api.v1.utils.database import mongo


class UserMongo:
    """User class for mongodb"""

    def __init__(self, *args, **kwargs):
        """Initialize User class"""
        self.email = kwargs.get('email')
        self.files = []
        self.verify_schema()

    def verify_schema(self):
        """Verify user schema"""
        USER_SCHEMA = {
            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "files": {"type": "array"},
            },
            "required": ["email", "files"]
        }
        # Validate user schema
        validate(instance=self.__dict__, schema=USER_SCHEMA)

    def save(self):
        """Save user to mongodb"""
        user = {
            "email": self.email,
            "files": self.files,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        return mongo.db.users.insert_one(user) # type: ignore
    
    def update(self, update_query):
        """Update user in mongodb"""
        return mongo.db.users.update_one({"email": self.email}, update_query) # type: ignore

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
