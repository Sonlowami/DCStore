from flask import jsonify

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
