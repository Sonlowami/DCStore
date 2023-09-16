import zipfile
from werkzeug.datastructures import FileStorage


def extract_and_return_dicom_list(zip_file):
    """Extract dicom files from zip file and return a list of dicom files"""
    dicoms_files = []
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.endswith('.dcm'):
                    file_stream = zip_ref.open(file)
                    dicoms_files.append(FileStorage(file_stream, file))
    except zipfile.BadZipFile:
        print('Error reading zip file')
    return dicoms_files
