from flask import jsonify

from api.v1.views import app_views
from api.v1.models.tables.user import User
from api.v1.models.tables.series import Series
from api.v1.models.tables.instance import Instance
from api.v1.utils.database import db
from api.v1.utils.token import authorize


@app_views.route('/instances', methods=['GET'])
@authorize
def get_instances_by_me(email: str) -> str:
    """Get instances of the doctor"""
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify([instance.to_dict() for instance in user.instances])


@app_views.route('/instances/<instance_id>', methods=['GET'])
@authorize
def get_instance_by_id(email: str, instance_id: str) -> str:
    """Get instance by id"""
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    instance = Instance.get_instance_by_sopInstanceUID(instance_id)
    if not instance or user not in instance.users:
        return jsonify({'error': 'Instance not found'}), 404
    
    return jsonify(instance.to_dict())


@app_views.route('/series/<series_id>/instances', methods=['GET'])
@authorize
def get_instances_by_series_id(email: str, series_id: str) -> str:
    """Get instances of the series"""
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    series = Series.get_series_by_seriesInstanceUID(series_id)
    if not series or user not in series.users:
        return jsonify({'error': 'Series not found'}), 404
    
    return jsonify([instance.to_dict() for instance in series.instances if user in instance.users])


@app_views.route('/series/<series_id>/instances/<instance_id>', methods=['GET'])
@authorize
def get_instance_by_series_id_and_instance_id(email: str, series_id: str, instance_id: str) -> str:
    """Get instance by series id and instance id"""
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    series = Series.get_series_by_seriesInstanceUID(series_id)
    if not series or user not in series.users:
        return jsonify({'error': 'Series not found'}), 404
    
    instance = Instance.get_instance_by_sopInstanceUID(instance_id)
    if (not instance) or (user not in instance.users) or (instance not in series.instances):
        return jsonify({'error': 'Instance not found'}), 404
    
    return jsonify(instance.to_dict())
