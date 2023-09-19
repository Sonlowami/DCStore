from flask import request, jsonify

from jsonschema import ValidationError
from datetime import datetime
from dotenv import load_dotenv
import os

from api.v1.views import app_views
from api.v1.models import File, User
from api.v1.models.tables import Patient, Study, Series, Instance
from api.v1.utils.zipping import zip_file, extract_and_return_dicom_list
from api.v1.utils.caching import redis_client
from api.v1.utils.database import mongo, db
from api.v1.utils.token import authorize

load_dotenv()

DICOM_FOLDER = os.getenv('DICOM_FOLDER', '/tmp/dicom_files')


@app_views.route('/files', methods=['POST'])
@authorize
def upload_file(email):
    """Upload dicom files to mongodb"""

    try:
        user = User.get_user(email)
    except Exception:
        return jsonify({'error': 'User not found'}), 404
    
    # Get all dicom files from request
    dicom_files = []
    for file in request.files.values():
        if file.filename.lower().endswith('.zip'):
            dicom_files += extract_and_return_dicom_list(file)
        elif file.filename.lower().endswith('.dcm'):
            dicom_files.append(file)
    if not dicom_files:
        return jsonify({'error': 'No dicom files provided'}), 400

    # Create folder if not exists
    os.makedirs(DICOM_FOLDER, exist_ok=True)

    # Save files to databases
    try:
        for file in dicom_files:

            # save to mongodb
            data = File.extract_metadata_from_dicom(file)
            if not data:
                return jsonify({'error': 'Invalid file'}), 400
            new_file = File(**data)
            if new_file.filepath:
                file.save(new_file.filepath)
                new_file.save()
            else:
                return jsonify({'error': 'Something went wrong!'}), 500
            
            # save to MySQL
            patient_data = Patient.extract_patient_metadata_from_file(new_file)
            existing_patient = Patient.get_patient_by_patientID(patient_data.get('patientID', ''))
            if existing_patient:
                patient = existing_patient
            else:
                patient = Patient(**patient_data)
                patient.save()

            study_data = Study.extract_study_metadata_from_file(new_file)
            existing_study = Study.get_study_by_studyInstanceUID(study_data.get('studyInstanceUID', ''))
            if existing_study:
                study = existing_study
            else:
                study = Study(**study_data)
                study.patient = patient
                study.save()

            series_data = Series.extract_series_metadata_from_file(new_file)
            existing_series = Series.get_series_by_seriesInstanceUID(series_data.get('seriesInstanceUID', ''))
            if existing_series:
                series = existing_series
            else:
                series = Series(**series_data)
                series.study = study
                series.save()

            instance_data = Instance.extract_instance_metadata_from_file(new_file)
            existing_instance = Instance.get_instance_by_sopInstanceUID(instance_data.get('sopInstanceUID', ''))
            if existing_instance:
                instance = existing_instance
            else:
                instance = Instance(**instance_data)
                instance.series = series
                instance.save()
            
            # Update user
            try:
                update_query = {
                    "$push": {
                        "files": new_file.filepath,
                        f"patients.{patient.patientID}": study.studyInstanceUID
                    },
                    "$set": {
                        "updated_at": datetime.now()
                    }
                }
                mongo.db.users.update_one({"email": email}, update_query)
            except Exception as e:
                print(e)
                return jsonify({'error': 'Something went wrong!'}), 500

            # generate or append to a zip
            # zip_folder = DICOM_FOLDER + '/zip'
            # if not os.path.exists(zip_folder):
            #     os.makedirs(zip_folder)
            # output_zip = f"{zip_folder}/{new_file.seriesInstanceUID}.zip"
            # zip_file(output_zip, file)
            # redis_client.set(new_file.seriesInstanceUID, output_zip)

        return jsonify({'message': 'File uploaded successfully'}), 201
    except ValidationError:
        return jsonify({'error': 'Invalid file'}), 400
