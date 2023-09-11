from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import text
from os import getenv
from dotenv import load_dotenv

from api.v1.utils.config import Config
from api.v1.utils.database import db
from api.v1.models import *


load_dotenv()

app = Flask(__name__)

# Configure app
app.url_map.strict_slashes = False
app.config.from_object(Config)

# Initialize database with migrations
db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def hello() -> str:
    return "Hello World!"

# Check database connection
@app.route("/db")
def db_check() -> str:
    try:
        db.session.execute(text("SELECT 1"))
        return "Database connected"
    except Exception as e:
        return "Database error: " + str(e)


if __name__ == "__main__":
    host = getenv('HOST', '0.0.0.0')
    port = getenv('PORT', 5000)
    debug = getenv('DEBUG', True)
    app.run(host=host, port=int(port), debug=bool(debug))
