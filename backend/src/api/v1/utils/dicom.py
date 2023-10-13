from flask import Request
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo

from typing import IO

from api.v1.models import File
from api.v1.models.tables import User


def get_all_dicom_files(request: Request) -> list:
    """
    Get all dicom files from request
    """
    from api.v1.utils.zipping import extract_and_return_dicom_list

    dicom_files = []
    for file in request.files.values():
        if file.filename.lower().endswith('.zip'):
            dicom_files += extract_and_return_dicom_list(file)
        elif file.filename.lower().endswith('.dcm'):
            dicom_files.append(file)
    return dicom_files


def save_file_to_mongodb(file: IO, user_mongo: dict) -> tuple[File, str]:
    """
    Extract metadata and save file in mongodb
    """
    data = File.extract_metadata_from_dicom(file)
    if not data:
        return None, None
    data['uploader_id'] = str(user_mongo['_id'])
    new_file = File(**data)
    file_id = new_file.save().inserted_id
    return new_file, file_id


def save_metadata_to_mysql_tables(new_file: File, db: SQLAlchemy, user: User) -> dict:
    """
    Save extracted metadata into mysql tables
    """
    from api.v1.models.tables import Patient, Study, Series, Instance
    from api.v1.utils.caching import redis_client

    patient_data = Patient.extract_patient_metadata_from_file(new_file)
    existing_patient = Patient.get_patient_by_patientID(patient_data.get('patientID', ''))
    new_patient = False
    if existing_patient:
        patient = existing_patient
    else:
        patient = Patient(**patient_data)
    if user not in patient.users:
        patient.users.append(user)
        new_patient = True

    study_data = Study.extract_study_metadata_from_file(new_file)
    existing_study = Study.get_study_by_studyInstanceUID(study_data.get('studyInstanceUID', ''))
    new_study = False
    if existing_study:
        study = existing_study
    else:
        study = Study(**study_data)
        study.patient = patient
    if user not in study.users:
        study.users.append(user)
        new_study = True

    series_data = Series.extract_series_metadata_from_file(new_file)
    existing_series = Series.get_series_by_seriesInstanceUID(series_data.get('seriesInstanceUID', ''))
    new_series = False
    if existing_series:
        series = existing_series
    else:
        series = Series(**series_data)
        series.study = study
    if user not in series.users:
        series.users.append(user)
        new_series = True

    instance_data = Instance.extract_instance_metadata_from_file(new_file)
    existing_instance = Instance.get_instance_by_sopInstanceUID(instance_data.get('sopInstanceUID', ''))
    new_instance = False
    if existing_instance:
        instance = existing_instance
    else:
        instance = Instance(**instance_data)
        instance.filepath = new_file.filepath
        instance.series = series
    if user not in instance.users:
        instance.users.append(user)
        new_instance = True
    
    db.session.add_all([patient, study, series, instance])
    db.session.commit()


    # update redis user info
    if new_patient:
        redis_client.incr(f'patients_count-{user.id}')
        if patient.patientSex == 'F' or patient.patientSex.lower() == 'female':
            redis_client.incr(f'female_patients_count-{user.id}')
        elif patient.patientSex == 'M' or patient.patientSex.lower() == 'male':
            redis_client.incr(f'male_patients_count-{user.id}')
        else:
            redis_client.incr(f'other_patients_count-{user.id}')
    if new_study:
        redis_client.incr(f'studies_count-{user.id}')
    if new_series:
        redis_client.incr(f'series_count-{user.id}')
    if new_instance:
        redis_client.incr(f'instances_count-{user.id}')

    return {
        "patient_data": patient_data,
        "study_data": study_data,
        "series_data": series_data,
        "instance_data": instance_data
    }


def add_to_user_files(email: str, filepath: str, mongo: PyMongo) -> bool:
    """
    add current filepath to user's files
    """
    from datetime import datetime

    try:
        update_query = {
            "$push": {
                "files": filepath,
            },
            "$set": {
                "updated_at": datetime.now()
            }
        }
        mongo.db.users.update_one({"email": email}, update_query)
        return True
    except Exception as e:
        print(e)
        return False


def process_file(file: IO, user: SQLAlchemy, user_mongo: dict, email: str):
    """
    Process a single file
    """
    from flask import jsonify

    from api.v1.utils.activity import RecentFiles
    from api.v1.utils.database import mongo, db

    new_file, file_id = save_file_to_mongodb(file, user_mongo)
    if not new_file or not file_id:
        return jsonify({'error': 'Invalid dicom file'}), 400
    data = save_metadata_to_mysql_tables(new_file, db, user)
    info = {
        "filename": file.filename,
        "patientName": data['patient_data'].get('patientName', ''),
        "studyDescription": data['study_data'].get('studyDescription', ''),
        "seriesDescription": data['series_data'].get('seriesDescription', ''),
        "instanceNumber": data['instance_data'].get('instanceNumber', ''),
        "sopInstanceUID": data['instance_data'].get('sopInstanceUID', ''),
        "action": "uploaded",
    }
    try:
        RecentFiles.add_file_to_recent_files(str(user_mongo['_id']), str(file_id), info)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Something went wrong!'}), 500
    if not add_to_user_files(email, new_file.filepath, mongo):
        return jsonify({'error': 'Something went wrong!'}), 500
