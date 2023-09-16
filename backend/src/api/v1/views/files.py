from flask import request, jsonify

from jsonschema import ValidationError
from dotenv import load_dotenv
import os

from api.v1.views import app_views
from api.v1.models import File
from api.v1.utils.zipping import zip_file, extract_and_return_dicom_list
from api.v1.utils.caching import redis_client
from api.v1.utils.database import mongo

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
            new_file.save()
            # generate or append to a zip
            zip_folder = DICOM_FOLDER + '/zip'
            if not os.path.exists(zip_folder):
                os.makedirs(zip_folder)
            output_zip = f"{zip_folder}/{new_file.seriesInstanceUID}.zip"
            zip_file(output_zip, file)
            redis_client.set(new_file.seriesInstanceUID, output_zip)

            return jsonify({'message': 'File uploaded successfully'}), 201
    except ValidationError:
        return jsonify({'error': 'Invalid file'}), 400
