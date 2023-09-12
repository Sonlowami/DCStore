from flask import request, jsonify
from werkzeug.security import check_password_hash

import datetime
import jwt
import json
from os import getenv
from typing import Dict

from api.v1.models.user import User
# from api.v1.utils.db import dbClient
dbClient = None
from api.v1.views import app_views


SECRET_KEY = getenv('SECRET_KEY')


@app_views.post('/login', strict_slashes=False)
def login() -> str:
    """Log a user inside the system"""
    try:
        user_data: Dict = request.get_json()
        valid_data: Dict = validate_login(user_data)
        email: str = valid_data['email']
        password: str = valid_data['password']
        user: User = dbClient.filter_by(email=email)
        print(user.return_value)
        print(check_password_hash.return_value)
        if check_password_hash(user.password, password):
            exp: datetime.Time = datetime.datetime.now() + datetime.timedelta(hours=24)
            token: str = jwt.encode({'email': email, 'exp': exp}, SECRET_KEY, algorithm='HS256')
            return jsonify({'x-token': token}), 200
        else:
            return jsonify({'error': 'Invalid password'}), 400
    except AttributeError:
        return jsonify({'error': 'user does not exist'}), 400
    except KeyError:
        return jsonify({'error': 'Missing email or password'}), 400
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON'}), 400
    except TypeError:
        return jsonify({'error': 'email and password must be string'}), 400


def validate_login(user_input: Dict) -> Dict:
    """Validate user input"""
    email:str = user_input['email']
    password: str = user_input['password']
    if not isinstance(email, str) or not isinstance(password, str):
        raise TypeError
    return {
        'email': email,
        'password': password
    }
