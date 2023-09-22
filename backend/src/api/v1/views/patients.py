from flask import jsonify

from api.v1.views import app_views
from api.v1.models.tables.user import User
from api.v1.models.tables.patient import Patient
from api.v1.models.tables.many_to_many import user_patient
from api.v1.utils.database import db
from api.v1.utils.token import authorize


@app_views.route('/patients', methods=['GET'])
@authorize
def get_patients_by_me(email: str) -> str:
    """Get patients of the doctor"""
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify([patient.to_dict() for patient in user.patients])


@app_views.route('/patients/<patient_id>', methods=['GET'])
@authorize
def get_patient_by_id(email: str,patient_id: str) -> str:
    """Get patient by id"""
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    patient = Patient.get_patient_by_patientID(patient_id)
    if not patient or user not in patient.users:
        return jsonify({'error': 'Patient not found'}), 404
    
    return jsonify(patient.to_dict())
    