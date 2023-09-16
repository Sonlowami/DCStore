import pydicom
import zipfile
import os
from typing import List


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
