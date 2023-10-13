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
            if redis_client.get(f'blacklist:{token}'):
                return jsonify({'error': 'Token has been blacklisted'}), 401
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            email = payload.get('email')
            if not email:
                return jsonify({'error': 'Invalid token payload'}), 401
            return f(email, *args, **kwargs)
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({'error': 'Invalid token signature'}), 401
        except jwt.exceptions.DecodeError:
            return jsonify({'error': 'Invalid token encoding'}), 401
        except Exception as e:
            print(e)
            return jsonify({'error': 'Something went wrong in view'}), 500
    return decorator
