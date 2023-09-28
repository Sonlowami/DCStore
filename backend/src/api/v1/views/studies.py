from flask import jsonify, send_file

from dotenv import load_dotenv
import os

from api.v1.views import app_views
from api.v1.models.tables.user import User
from api.v1.models.tables.study import Study
from api.v1.models.tables.patient import Patient
from api.v1.utils.database import db
from api.v1.utils.token import authorize


load_dotenv()

DICOM_FOLDER = os.getenv('DICOM_FOLDER', '/tmp/dicom_files')


@app_views.route('/studies', methods=['GET'])
@authorize
def get_studies_by_me(email: str) -> str:
    """Get studies of the doctor"""
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify([study.to_dict() for study in user.studies])


@app_views.route('/studies/<study_id>', methods=['GET'])
@authorize
def get_study_by_id(email: str, study_id: str) -> str:
    """Get study by id"""
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    study = Study.get_study_by_studyInstanceUID(study_id)
    if not study or user not in study.users:
        return jsonify({'error': 'Study not found'}), 404
    
    return jsonify(study.to_dict())


@app_views.route('/patients/<patient_id>/studies', methods=['GET'])
@authorize
def get_studies_by_patient_id(email: str, patient_id: str) -> str:
    """Get studies of the patient"""
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    patient = Patient.get_patient_by_patientID(patient_id)
    if not patient or user not in patient.users:
        return jsonify({'error': 'Patient not found'}), 404
    
    return jsonify([study.to_dict() for study in patient.studies if user in study.users])

@app_views.route('/patients/<patient_id>/studies/<study_id>', methods=['GET'])
@authorize
def get_study_by_patient_id_and_study_id(email: str, patient_id: str, study_id: str) -> str:
    """Get study by patient id and study id"""
    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    patient = Patient.get_patient_by_patientID(patient_id)
    if not patient or user not in patient.users:
        return jsonify({'error': 'Patient not found'}), 404
    
    study = Study.get_study_by_studyInstanceUID(study_id)
    if (not study) or (user not in study.users) or (study not in patient.studies):
        return jsonify({'error': 'Study not found'}), 404
    
    return jsonify(study.to_dict())


@app_views.route('/studies/<study_id>/download', methods=['GET'])
# @authorize
def download_study(study_id: str) -> str:
# def download_study(email: str, study_id: str) -> str:
    """Download study"""
    # user = User.get_user(email)
    # if not user:
    #     return jsonify({'error': 'User not found'}), 404
    
    study = Study.get_study_by_studyInstanceUID(study_id)
    # if not study or user not in study.users:
    if not study:
        return jsonify({'error': 'Study not found'}), 404

    zip_path = f'{DICOM_FOLDER}/zip/{study_id}.zip'
    try:
        return send_file(zip_path, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'Study not found'}), 404
