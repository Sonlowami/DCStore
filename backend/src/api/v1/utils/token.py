from flask import request, jsonify

import jwt
from functools import wraps
from os import getenv
from dotenv import load_dotenv

from api.v1.utils.caching import redis_client


load_dotenv()

SECRET_KEY = getenv('SECRET_KEY', '')


def authorize(f):
    """Check if a token sent by the user is valid"""
    @wraps(f)
    def decorator(*args, **kwargs):
        """Inner function to handle the be returned as a decorator"""
        token: str = request.headers.get('x-token', '')
        try:
            assert not redis_client.get(f'blacklist:{token}')
            email: str = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])['email']
            return f(email, *args, **kwargs)
        except Exception as e:
            print(e)
            return ({'error': 'Invalid token'}), 401
    return decorator
