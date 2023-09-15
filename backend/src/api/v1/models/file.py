from jsonschema import validate
from datetime import datetime
from uuid import uuid4
from dotenv import load_dotenv
import os
import pydicom

from api.v1.utils.database import mongo

load_dotenv()

DICOM_FOLDER = os.getenv('DICOM_FOLDER', '/tmp/dicom_files')


class File:
    """File class for mongodb"""

    def __init__(self, *args, **kwargs):
        """Initialize File class"""
        self.filename = kwargs.get('filename')
        self.filepath = kwargs.get('filepath')
        self.filesize = kwargs.get('filesize')
        self.patient_owners = kwargs.get('patient_owner')
        self.physician_owners = kwargs.get('physician_owners')
        self.metadata = kwargs.get('metadata')
        self.verify_schema()
    
    def verify_schema(self):
        """Verify file schema"""
        FILE_SCHEMA = {
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "filepath": {"type": "string"},
                "filesize": {"type": "number"},
                "uploadDate": {
                    "type": "string",
                    "format": "date-time"
                },
                "patient_owner": {"type": "object"},
                "physician_owners": {"type": "array"},
                "metadata": {"type": "object"}
            },
            # "required": ["filename", "filepath", "patient_owners", "physician_owners", "metadata"]
            "required": ["filename", "filepath", "metadata"]
        }
        validate(instance=self.__dict__, schema=FILE_SCHEMA)
    
    def save(self):
        """Save file to mongodb"""
        file = {
            "filename": self.filename,
            "filepath": self.filepath,
            "filesize": self.filesize,
            "uploadDate": datetime.now(),
            "patient_owners": self.patient_owner,
            "physician_owners": self.physician_owners,
            "metadata": self.metadata
        }
        return mongo.db.files.insert_one(file) # type: ignore
    
    @staticmethod
    def get_file_by_id(id):
        """Get file from mongodb"""
        file = mongo.db.files.find_one({"_id": id}) # type: ignore
        return file

    @staticmethod
    def extract_metadata_from_dicom(dicom_file):
        """Extract metadata from a DICOM file and return a dictionary."""
        try:
            # Load the DICOM file using pydicom
            dcm = pydicom.dcmread(dicom_file)

            # Extract metadata from the DICOM file
            metadata = {
                "filename": dicom_file.filename if dicom_file.filename else 'untitled',
                "filepath": os.path.join(DICOM_FOLDER, f'{str(uuid4())}.dcm'),
                "filesize": len(dicom_file.read()),
                "uploadDate": datetime.now(),
                "metadata": {
                    "patientName": str(dcm.PatientName),
                    "patientID": str(dcm.PatientID),
                    "patientBirthDate": datetime.strptime(str(dcm.PatientBirthDate), '%Y%m%d') if dcm.PatientBirthDate else None,
                    "patientSex": str(dcm.PatientSex),
                    "patientAge": str(dcm.PatientAge) if dcm.PatientAge else None,
                    "studyDescription": str(dcm.StudyDescription),
                    "studyDate": datetime.strptime(str(dcm.StudyDate), '%Y%m%d') if dcm.StudyDate else None,
                    "studyInstanceUID": str(dcm.StudyInstanceUID),
                    "seriesDescription": str(dcm.SeriesDescription),
                    "seriesInstanceUID": str(dcm.SeriesInstanceUID),
                    "seriesNumber": str(dcm.seriesNumber),
                    "modality": str(dcm.Modality),
                    "instanceNumber": str(dcm.instanceNumber),
                    "sopInstanceUID": str(dcm.SOPInstanceUID),
                    "physicianName": str(dcm.PhysiciansName) if dcm.get("PhysiciansName") else '',
                    "imageType": [str(val) for val in dcm.ImageType] if dcm.get("ImageType") else [],
                },
            }
            return metadata
        except Exception as e:
            # Handle any exceptions here (e.g., invalid DICOM format)
            print(f"Error extracting metadata from DICOM: {str(e)}")
            return None
