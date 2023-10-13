from flask import request, jsonify, send_file

from jsonschema import ValidationError
from datetime import datetime
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId
from bson.errors import InvalidId

from api.v1.views import app_views
from api.v1.models import File, UserMongo
from api.v1.models.tables import Instance, User
from api.v1.utils.dicom import get_all_dicom_files, process_file
from api.v1.utils.activity import RecentFiles
from api.v1.utils.database import mongo
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

    dicom_files = get_all_dicom_files(request)
    if not dicom_files:
        return jsonify({'error': 'No dicom files provided'}), 400
    os.makedirs(DICOM_FOLDER, exist_ok=True)
    try:
        for file in dicom_files:
            process_file(file, user, user_mongo, email)
        return jsonify({'message': 'File(s) uploaded successfully'}), 201
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
