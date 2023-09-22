from flask import jsonify

from api.v1.views import app_views
from api.v1.models.tables.user import User
from api.v1.models.tables.study import Study
from api.v1.models.tables.series import Series
from api.v1.utils.database import db
from api.v1.utils.token import authorize


@app_views.route('/series', methods=['GET'])
@authorize
def get_series_by_me(email: str) -> str:
    """Get series of the doctor"""
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify([series.to_dict() for series in user.series])


@app_views.route('/series/<series_id>', methods=['GET'])
@authorize
def get_series_by_id(email: str, series_id: str) -> str:
    """Get series by id"""
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    series = Series.get_series_by_seriesInstanceUID(series_id)
    if not series or user not in series.users:
        return jsonify({'error': 'Series not found'}), 404
    
    return jsonify(series.to_dict())


@app_views.route('/studies/<study_id>/series', methods=['GET'])
@authorize
def get_series_by_study_id(email: str, study_id: str) -> str:
    """Get series of the study"""
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    study = Study.get_study_by_studyInstanceUID(study_id)
    if not study or user not in study.users:
        return jsonify({'error': 'Study not found'}), 404
    
    return jsonify([series.to_dict() for series in study.series if user in series.users])


@app_views.route('/studies/<study_id>/series/<series_id>', methods=['GET'])
@authorize
def get_series_by_study_id_and_series_id(email: str, study_id: str, series_id: str) -> str:
    """Get series by study id and series id"""
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    study = Study.get_study_by_studyInstanceUID(study_id)
    if not study or user not in study.users:
        return jsonify({'error': 'Study not found'}), 404
    
    series = Series.get_series_by_seriesInstanceUID(series_id)
    if (not series) or (user not in series.users) or (series not in study.series):
        return jsonify({'error': 'Series not found'}), 404
    
    return jsonify(series.to_dict())
