from flask import Flask, jsonify, request

from os import getenv
from dotenv import load_dotenv

from api.v1.utils.database import mongo
from api.v1.utils.config import Config
from api.v1.models.user import User


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

# Insert todo item into MongoDB
@app.route('/todo', methods=['GET'])
def insert_todo():
    todo = {
        'title': 'Test todo',
        'description': 'Test todo description',
        'done': False,
    }
    mongo.db.todos.insert_one(todo) # type: ignore
    return 'Todo inserted!'

# Get all todo items from MongoDB
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = mongo.db.todos.find() # type: ignore
    return jsonify([todo['title'] for todo in todos])

# Get all users from MongoDB
@app.route('/users', methods=['GET'])
def get_users():
    users = User.get_users()
    return jsonify(users)

# Create user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        user = User(
            email=data.get('email'),
            password=data.get('password'),
            username=data.get('username'),
            fullname=data.get('fullname'),
            role=data.get('role'),
        )
    except Exception as e:
        return jsonify( { "error": "Invalid user schema" } ), 400
    User.save(user)
    return jsonify(user), 201


if __name__ == '__main__':
    host = getenv('HOST', 'localhost')
    port = getenv('PORT', 5000)
    app.run(host=host, port=int(port))
