from flask import request, jsonify
from werkzeug.security import generate_password_hash

import datetime
import json
from jsonschema import ValidationError

from api.v1.models.user import User
from api.v1.views import app_views


@app_views.post('/register')
def register() -> str:
    """Register a new user"""
    try:
        user_data = request.get_json()
        user_by_email = User.get_user(user_data.get('email', ''))
        user_by_username = User.get_user_by_username(user_data.get('username', ''))
        if user_by_email or user_by_username:
            return jsonify({'error': 'User already exists'}), 400
        user = User(**user_data)
        user.save()
        return jsonify({'message': 'Account created successfully!'}), 201

    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON'}), 400
    except ValidationError:
        return jsonify({'error': 'Missing required information'}), 400
    except (TypeError, ValueError) as e:
        return jsonify({'error': e}), 400
