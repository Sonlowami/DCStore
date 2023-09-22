from api.v1.views import app_views
from flask import jsonify, request
from api.v1.models.tables.user import User
from api.v1.utils.caching import redis_client
from api.v1.utils.token import authorize


@app_views.route('/logout', methods=['GET'])
@authorize
def logout(email):
    """Log out a user"""
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    token = request.headers.get('x-token', '')
    redis_client.setex(f'blacklist:{token}', 60 * 60 * 24, '1')
    return jsonify({'message': 'Logged out'}), 200
