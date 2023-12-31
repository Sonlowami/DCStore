from bson.objectid import ObjectId
from flask import request, jsonify
from api.v1.models.user import User
from api.v1.models.file import File
from api.v1.utils.database import mongo
from api.v1.utils.caching import redis_client
from api.v1.utils.token import authorize
from api.v1.views import app_views


@app_views.get('/studies')
@authorize
def get_studies_by_me(email: str, page: int = 0) -> str:
    """Get studies of the patient or done by the doctor"""
    user: User = User.get_user(email)
    try:
        conditions = [
            {'$match': {
                'uploader_id': user._id
            } },
            {'$limit': 20},
            {'$skip': (page * 20)},
            {'$group': 'seriesNumber'}
        ]
        studies = mongo.db.files.aggregate(comditions)
        return jsonify(studies), 200
    except Exception as e:
        return jsonify({'error': e}), 500


@app_views.get('/studies/<id>')
@authorize
def get_one_study(email: str, id: str) -> str:
    """Get one study with the given id"""
    try:
        user = User.get_user(email)
        study = mongo.db.files.find_one({'metadata.studyInstanceUID': id})
        if str(user._id) == str(study.uploader_id):
            return jsonify(study), 200
    except Exception as e:
        return jsonify({'error': e}), 500


@app_views.get('/series/<id>')
@authorize
def get_one_study(email: str, id: str) -> str:
    """Get one series with the given id"""
    try:
        user = User.get_user(email)
        series = mongo.db.files.find_one({'metadata.seriesInstanceUID': id})
        if str(user._id) == str(series.uploader_id):
            return jsonify(series), 200
    except Exception as e:
        return jsonify({'error': e}), 500
