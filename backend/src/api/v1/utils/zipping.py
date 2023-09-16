import os
import pydicom
from typing import List
from werkzeug.datastructures import FileStorage
import zipfile


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

def zip_file(output_zip: str, filepaths: List) -> str:
    """Zip given files into a new zip or append to zip file"""
    if zipfile.is_zipfile(output_zip):
        return append_to_zip(output_zip, filepaths)
    else:
        return write_to_zip(output_zip, filepaths)


def write_to_zip(output: str, filepaths: List) -> str:
    """write to a new zipfile"""
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for filepath in filepaths:
            zipf.write(output, os.path.basename(filepath))
    return output


def append_to_zip(output: str, filepaths: List) -> str:
    """append to an already existing zipfile"""
    with zipfile.ZipFile(output, 'a', zipfile.ZIP_DEFLATED) as zipf:
        for filepath in filepaths:
            zipf.write(output, os.path.basename(filepath))
    return output
