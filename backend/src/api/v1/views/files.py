from flask import request, jsonify

from jsonschema import ValidationError
from dotenv import load_dotenv
import os

from api.v1.views import app_views
from api.v1.models import File
from api.v1.utils.database import mongo
from api.v1.utils.zip import extract_and_return_dicom_list


load_dotenv()

DICOM_FOLDER = os.getenv('DICOM_FOLDER', '/tmp/dicom_files')


@app_views.route('/files', methods=['POST'])
def upload_file():
    """Upload dicom files to mongodb"""
    
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

    # Save files to mongodb
    try:
        for file in dicom_files:
            data = File.extract_metadata_from_dicom(file)
            if not data:
                return jsonify({'error': 'Invalid file'}), 400
            new_file = File(**data)
            if new_file.filepath:
                file.save(new_file.filepath)
                new_file.save()
            else:
                return jsonify({'error': 'Something went wrong!'}), 500
        return jsonify({'message': 'File(s) uploaded successfully'}), 201
    except ValidationError:
        return jsonify({'error': 'Invalid file'}), 400
