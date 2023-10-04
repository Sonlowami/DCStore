from flask import jsonify, request

import json

from api.v1.views import app_views
from api.v1.models.tables.user import User
from api.v1.models.user import UserMongo
from api.v1.utils.token import authorize
from api.v1.utils.caching import redis_client


VALID_INFO = ['patients', 'studies', 'series', 'instances']


@app_views.route('/dicom_info', methods=['GET'])
@authorize
def dicom_info(email):
    """
    Get dicom info
    """
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    any_valid_param = any(
        request.args.get(param, '').strip().lower() == 'true'
        for param in VALID_INFO
    )
    info = {}

    if (any_valid_param and request.args.get('patients', '').strip().lower() == 'true') \
            or not any_valid_param:
        total_patients = redis_client.get(f'patients_count-{user.id}')
        info['total_patients'] = int(total_patients) if total_patients else 0
    if (any_valid_param and request.args.get('studies', '').strip().lower() == 'true') \
            or not any_valid_param:
        total_studies = redis_client.get(f'studies_count-{user.id}')
        info['total_studies'] = int(total_studies) if total_studies else 0
    if (any_valid_param and request.args.get('series', '').strip().lower() == 'true') \
            or not any_valid_param:
        total_series = redis_client.get(f'series_count-{user.id}')
        info['total_series'] = int(total_series) if total_series else 0
    if (any_valid_param and request.args.get('instances', '').strip().lower() == 'true') \
            or not any_valid_param:
        total_instances = redis_client.get(f'instances_count-{user.id}')
        info['total_instances'] = int(total_instances) if total_instances else 0
    
    return jsonify(info), 200


@app_views.route('/recent_files', methods=['GET'])
@authorize
def recent_files(email):
    """
    Get recent activities
    """
    user = UserMongo.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    recent_activities = redis_client.hgetall(f'recent_files:{str(user["_id"])}')
    try:
        recent = []
        for key, value in recent_activities.items():
            recent.append({
                'fileID': key.decode('utf-8'),
                'info': json.loads(value.decode('utf-8'))
            })
        return jsonify(recent), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Something went wrong'}), 500


@app_views.route('/patients_gender_count', methods=['GET'])
@authorize
def patients_gender_count(email):
    """
    Get gender count for patients
    """
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        gender_count = {}
        gender_count['males'] = redis_client.get(f'male_patients_count-{user.id}')
        if gender_count['males']:
            gender_count['males'] = int(gender_count['males'].decode('utf-8'))
        else:
            gender_count['males'] = 0
        gender_count['females'] = redis_client.get(f'female_patients_count-{user.id}')
        if gender_count['females']:
            gender_count['females'] = int(gender_count['females'].decode('utf-8'))
        else:
            gender_count['females'] = 0
        gender_count['others'] = redis_client.get(f'other_patients_count-{user.id}')
        if gender_count['others']:
            gender_count['others'] = int(gender_count['others'].decode('utf-8'))
        else:
            gender_count['others'] = 0
        return jsonify(gender_count), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Something went wrong'}), 500
