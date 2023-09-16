from flask import request, jsonify
from api.v1.models.user import User
from api.v1.models.file import File
from api.v1.utils.database import mongo
from api.v1.utils.caching import redis_client
from api.v1.utils.token import authorize
from api.v1.views import app_views


@app_views.get('/studies')
def get_studies_by_me(email: str, page: int = 0) -> str:
    """Get studies of the patient or done by the doctor"""
    user: User = User.get_user(email)
    try:
        conditions = [
            {'$match': {
                'uploader_id': user._id
            } },
            {'$limit': 20},
            {'$skip': (page * 20)}
        ]
        studies = mongo.db.users.aggregate(comditions)
        return jsonify(studies), 200
    except Exception as e:
        return jsonify({'error': e}), 500
