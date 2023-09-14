from flask import Flask

from os import getenv
from dotenv import load_dotenv

from api.v1.utils.database import mongo
from api.v1.utils.config import Config


# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
# Load configuration
app.config.from_object(Config)
# Connect to MongoDB database
mongo.init_app(app)


@app.route('/')
def index():
    return 'Hello World!'


if __name__ == '__main__':
    host = getenv('HOST', 'localhost')
    port = getenv('PORT', 5000)
    app.run(host=host, port=int(port))
