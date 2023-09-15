from flask import Flask, jsonify
from flask_mail import Mail
from flask_cors import CORS
from flasgger import Swagger

from os import getenv
from dotenv import load_dotenv

from api.v1.utils.config import Config
from api.v1.utils.database import mongo
from api.v1.views import app_views


load_dotenv()

app = Flask(__name__)

# Configure app
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
app.config.from_object(Config)

# Initialize database
mongo.init_app(app)
# Initialize mail
# mail = Mail(app)  # TODO: Uncomment this line when ready
# Initialize Swagger
Swagger(app)
# Initialize CORS
CORS(app)


@app.route("/")
def hello() -> str:
    return "Hello World!"


if __name__ == "__main__":
    host = getenv('HOST', '0.0.0.0')
    port = getenv('PORT', 5000)
    app.run(host=host, port=int(port))
