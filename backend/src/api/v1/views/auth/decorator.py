import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError

from flask import request, jsonify
from functools import wraps
from os import getenv


SECRET_KEY = getenv('SECRET_KEY', '')


def authorize(f):
    """Check if a token sent by the user is valid"""
    @wraps(f)
    def decorator(*args, **kwargs) -> callable:
        """Inner function to handle the be returned as a decorator"""
        token: str = request.headers.get('x-token') or request.args.get('x-token')
        try:
            email: str = jwt.decode(token, SECRET_KEY, algorithm='HS256')['email']
            return f(email, *args, **kwargs)
        except ExpiredSignatureError:
            return jsonify({'error': 'token expired'}), 403
        except DecodeError:
            return ({'error': 'Invalid token'}), 403
    return decorator
