from flask import Flask, jsonify
from flask_mail import Mail
from flask_cors import CORS
from flasgger import Swagger

from os import getenv
from dotenv import load_dotenv

from api.v1.utils.config import Config
from api.v1.utils.database import mongo, db
from api.v1.views import app_views


load_dotenv()

app = Flask(__name__)

# Configure app
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
app.config.from_object(Config)

# Initialize databases
db.init_app(app)
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

from sqlalchemy import text
# Test database connection
@app.route('/test_mysql')
def test_mysql():
    try:
        db.session.execute(text('SELECT 1'))
        return jsonify({'message': 'Mysql connection success'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'er'}), 500

# test mongodb connection
@app.route('/test_mongodb')
def test_mongodb():
    try:
        mongo.db.command('ping')
        return jsonify({'message': 'Mongodb connection success'}), 200
    except Exception as e:
        return jsonify({'error': e}), 500


if __name__ == "__main__":
    host = getenv('HOST', '0.0.0.0')
    port = getenv('PORT', 5000)
    app.run(host=host, port=int(port))
