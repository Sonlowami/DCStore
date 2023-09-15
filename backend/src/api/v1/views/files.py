from flask import request, jsonify

from jsonschema import ValidationError
from dotenv import load_dotenv
import os

from api.v1.views import app_views
from api.v1.models import File


load_dotenv()

DICOM_FOLDER = os.getenv('DICOM_FOLDER', '/tmp/dicom_files')


@app_views.route('/files', methods=['POST'])
def upload_file():
    """Upload file to mongodb"""
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 400
    try:
        data = File.extract_metadata_from_dicom(file)
        if not data:
            return jsonify({'error': 'Invalid file'}), 400
        new_file = File(**data)
        if new_file.filepath:
            # Create folder if not exists
            if not os.path.exists(DICOM_FOLDER):
                os.makedirs(DICOM_FOLDER)
            file.save(new_file.filepath)
        else:
            return jsonify({'error': 'Something went wrong!'}), 500
        new_file.save()
        return jsonify({'message': 'File uploaded successfully'}), 201
    except ValidationError:
        return jsonify({'error': 'Invalid file'}), 400
