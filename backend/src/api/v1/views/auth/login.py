from flask import request, jsonify
from werkzeug.security import check_password_hash

import datetime
import jwt
from os import getenv
from dotenv import load_dotenv

from api.v1.models.user import User
from api.v1.views import app_views


load_dotenv()

SECRET_KEY = getenv('SECRET_KEY', '')


@app_views.post('/login')
def login() -> str:
    """Log a user inside the system"""
    if not request.is_json:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    user_data = request.get_json()
    email = user_data.get('email', '')
    if not email:
        return jsonify({'error': 'Missing email'}), 400
    password = user_data.get('password', '')
    if not password:
        return jsonify({'error': 'Missing password'}), 400
    
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User does not exist'}), 400
    if not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Invalid password'}), 400
    try:
        exp = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        token = jwt.encode({'email': email, 'exp': exp}, SECRET_KEY, algorithm='HS256')
        return jsonify({'x-token': token}), 201
    except Exception:
        pass
    return jsonify({'error': 'Something went wrong'}), 500
