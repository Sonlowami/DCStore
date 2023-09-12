from flask import request, jsonify
from werkzeug.security import generate_password_hash

import datetime
import json
from typing import Dict

from api.v1.models.user import User
from api.v1.views import app_views


@app_views.post('/register', strict_slashes=False)
def register() -> str:
    """Register a new user"""
    try:
        user_data: Dict = request.get_json()
        valid_data: Dict = validate_info(user_data)
        user = User(**valid_data)
        user.save()
        return jsonify({'message': 'Account created successfully!'}), 201

    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON'}), 400
    except KeyError:
        return jsonify({'error': 'Missing required information'}), 400
    except (TypeError, ValueError) as e:
        return jsonify({'error': e})


def validate_info(user_input: Dict) -> Dict:
    """Validate user input"""
    first_name: str = user_input['first_name']
    last_name: str = user_input['last_name']
    email: str = user_input['email']
    password: str = hash_password(user_input['password'])
    birthday: Date = create_date(user_input['birthday'])
    category: str = user_input['category']

    if not isinstance(first_name, str) or not isinstance(last_name, str):
        raise TypeError
    if not isinstance(email, str) or not isinstance(password, str):
        raise TypeError
    if category not in ['patient', 'hcprovider']:
        raise ValueError
    return {'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'birthday': birthday,
            'category': category
    }

def hash_password(password: str) -> str:
    """Hash a password"""
    return generate_password_hash(password)

def create_date(date_str: str) -> datetime.date:
    """Create a date object"""
    format: str = '%Y-%m-%d'
    return datetime.strftime(date_str, format).date()
