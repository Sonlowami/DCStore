from flask import jsonify, request

from api.v1.views import app_views
from api.v1.models.tables.user import User
from api.v1.utils.token import authorize


@app_views.route('/profile', methods=['GET'])
@authorize
def get_profile(email):
    """Get user profile"""
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


@app_views.route('/profile', methods=['PUT'])
@authorize
def update_profile(email):
    """Update user profile"""
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    
    data = request.get_json()
    try:
        user.update_user(**data)
        return jsonify(user.to_dict()), 200
    except Exception as e:
        if str(e) == 'Username already exists':
            return jsonify({'error': 'Username already exists'}), 400
        elif str(e) == 'Email already exists':
            return jsonify({'error': 'Email already exists'}), 400
        else:
            print(e)
            return jsonify({'error': 'Something went wrong!'}), 500
