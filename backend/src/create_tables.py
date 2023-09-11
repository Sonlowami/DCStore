from api.v1.app import app
from api.v1.utils.database import db

with app.app_context():
    db.create_all()
