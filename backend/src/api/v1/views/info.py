from flask import jsonify, request

from api.v1.views import app_views
from api.v1.models.tables.user import User
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
