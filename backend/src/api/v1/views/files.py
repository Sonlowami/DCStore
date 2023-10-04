from flask import request, jsonify, send_file

from jsonschema import ValidationError
from datetime import datetime
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId, InvalidId

from api.v1.views import app_views
from api.v1.models import File, UserMongo
from api.v1.models.tables import Patient, Study, Series, Instance, User
from api.v1.utils.zipping import zip_file, extract_and_return_dicom_list
from api.v1.utils.caching import redis_client
from api.v1.utils.activity import RecentFiles
from api.v1.utils.database import mongo, db
from api.v1.utils.token import authorize

load_dotenv()

DICOM_FOLDER = os.getenv('DICOM_FOLDER', '/tmp/dicom_files')


@app_views.route('/files', methods=['POST'])
@authorize
def upload_file(email):
    """Upload dicom files to mongodb"""

    user = User.get_user(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user_mongo = UserMongo.get_user(email)
    
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

            # save file to mongodb
            data = File.extract_metadata_from_dicom(file)
            if not data:
                return jsonify({'error': 'Invalid file'}), 400
            data['uploader_id'] = str(user_mongo['_id'])
            new_file = File(**data)
            file_id = new_file.save().inserted_id
            
            # save metadata to MySQL
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

            # update recent files
            info = {
                "filename": file.filename,
                "patientName": patient_data.get('patientName', ''),
                "studyDescription": study_data.get('studyDescription', ''),
                "seriesDescription": series_data.get('seriesDescription', ''),
                "instanceNumber": instance_data.get('instanceNumber', ''),
                "sopInstanceUID": instance_data.get('sopInstanceUID', ''),
                "action": "uploaded",
            }
            try:
                RecentFiles.add_file_to_recent_files(str(user_mongo['_id']), str(file_id), info)
            except Exception as e:
                print(e)
                return jsonify({'error': 'Something went wrong!'}), 500
            
            # Update user
            try:
                update_query = {
                    "$push": {
                        "files": new_file.filepath,
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
            zip_folder = DICOM_FOLDER + '/zip'
            os.makedirs(zip_folder, exist_ok=True)
            output_zip =f"{zip_folder}/{new_file.metadata['studyInstanceUID']}.zip"
            zip_file(output_zip, file)
            redis_client.set(new_file.metadata['seriesInstanceUID'], output_zip)

        return jsonify({'message': 'File uploaded successfully'}), 201
    except ValidationError:
        return jsonify({'error': 'Invalid file'}), 400


@app_views.route('/files', methods=['GET'])
@authorize
def get_files(email):
    """Get all files uploaded by a user"""
    try:
        user = UserMongo.get_user(email)
    except Exception:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        files = mongo.db.files.find({"uploader_id": str(user['_id'])})
        return jsonify([File.serialize_file(file) for file in files]), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Something went wrong!'}), 500


@app_views.route('/files/<file_id>', methods=['GET'])
@authorize
def get_file(email, file_id):
    """Get a file uploaded by a user"""
    try:
        user = UserMongo.get_user(email)
    except Exception:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        file = mongo.db.files.find_one({"_id": ObjectId(file_id), "uploader_id": str(user['_id'])})
        if not file:
            return jsonify({'error': 'File not found'}), 404
        return jsonify(File.serialize_file(file)), 200
    except InvalidId:
        return jsonify({'error': 'Invalid file id'}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': 'Something went wrong!'}), 500


@app_views.route('/files/<file_id>', methods=['DELETE'])
@authorize
def delete_file(email, file_id):
    """Delete a file uploaded by a user"""
    try:
        user = UserMongo.get_user(email)
    except Exception:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        # delete file from mongodb
        file = mongo.db.files.find_one({"_id": ObjectId(file_id), "uploader_id": str(user['_id'])})
        if not file:
            return jsonify({'error': 'File not found'}), 404
        mongo.db.files.delete_one({"_id": ObjectId(file_id)})

        # remove file from user's files
        try:
            update_query = {
                "$pull": {
                    "files": file['filepath']
                },
                "$set": {
                    "updated_at": datetime.now()
                }
            }
            mongo.db.users.update_one({"email": email}, update_query)
        except Exception as e:
            print(e)
            return jsonify({'error': 'Something went wrong!'}), 500
        
        # remove file from MySQL
        try:
            instance = Instance.get_instance_by_sopInstanceUID(file['metadata']['sopInstanceUID'])
            instance.delete()
        except Exception as e:
            print(e)
            return jsonify({'error': 'Something went wrong!'}), 500
        
        # remove file from filesystem
        try:
            os.remove(file['filepath'])
        except Exception as e:
            print(e)
            return jsonify({'error': 'Something went wrong!'}), 500
        return jsonify({'message': 'File deleted successfully'}), 200
    except InvalidId:
        return jsonify({'error': 'Invalid file id'}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': 'Something went wrong!'}), 500


@app_views.route('/files/<file_id>/download', methods=['GET'])
@authorize
def download_file(email, file_id):
    """Download a file uploaded by a user"""
    try:
        user = UserMongo.get_user(email)
    except Exception:
        return jsonify({'error': 'User not found'}), 404
    
    try:
        file = mongo.db.files.find_one({"_id": ObjectId(file_id), "uploader_id": str(user['_id'])})
        if not file:
            return jsonify({'error': 'File not found'}), 404

        info = {
            "filename": file['filename'],
            "patientName": file['metadata'].get('patientName', ''),
            "studyDescription": file['metadata'].get('studyDescription', ''),
            "seriesDescription": file['metadata'].get('seriesDescription', ''),
            "instanceNumber": file['metadata'].get('instanceNumber', ''),
            "sopInstanceUID": file['metadata'].get('sopInstanceUID', ''),
            "action": "downloaded",
        }
        RecentFiles.add_file_to_recent_files(str(user['_id']), file_id, info)
        return send_file(file['filepath'], as_attachment=True), 200
    except InvalidId:
        return jsonify({'error': 'Invalid file id'}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': 'Something went wrong!'}), 500
