from flask import request, jsonify
from werkzeug.security import generate_password_hash

import datetime
import json
from jsonschema import ValidationError

from api.v1.models.user import UserMongo
from api.v1.models.tables.user import User
from api.v1.views import app_views


@app_views.post('/register')
def register() -> str:
    """Register a new user"""
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    
    user_json = request.get_json()
    if User.get_user(user_json.get('email', '')):
        return jsonify({'error': 'User already exists'}), 400
    if User.get_user_by_username(user_json.get('username', '')):
        return jsonify({'error': 'Username already exists'}), 400
    try:
        user = User(**user_json)
        user.save()
        user_mongo = UserMongo(email=user.email)
        user_mongo.save()
        return jsonify({'message': 'User created'}), 201
    except ValidationError as e:
        return jsonify({'error': f'Invalid schema. {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400
