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
        self.patient_owner = kwargs.get('patient_owner', {})
        self.physician_owners = kwargs.get('physician_owners', [])
        self.metadata = kwargs.get('metadata')
        self.uploader_id = kwargs.get('uploader_id')
        self.verify_schema()
    
    def verify_schema(self):
        """Verify file schema"""
        FILE_SCHEMA = {
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "filepath": {"type": "string"},
                "uploadDate": {
                    "type": "string",
                    "format": "date-time"
                },
                "patient_owner": {"type": "object"},
                "physician_owners": {"type": "array"},
                "metadata": {"type": "object"},
                "uploader_id": {"type": "string"},
            },
            "required": ["filename", "filepath", "metadata", "uploader_id"]
        }
        validate(instance=self.__dict__, schema=FILE_SCHEMA)
    
    def to_dict(self):
        """Convert file object to dictionary"""
        dict = self.__dict__.copy()
        for key, value in dict.items():
            if key == '_id':
                dict[key] = str(value)
            if isinstance(value, datetime):
                dict[key] = value.isoformat()
        try:
            del dict['filepath']
        except KeyError:
            pass
        return dict
    
    def save(self):
        """Save file to mongodb"""
        file = {
            "filename": self.filename,
            "filepath": self.filepath,
            "uploadDate": datetime.now(),
            "patient_owners": self.patient_owner,
            "physician_owners": self.physician_owners,
            "metadata": self.metadata,
            "uploader_id": self.uploader_id,
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
                "filename": str(dicom_file.filename).split('/')[-1] if dicom_file.filename else 'untitled',
                "filepath": os.path.join(DICOM_FOLDER, f'{str(uuid4())}.dcm'),
                "uploadDate": datetime.now(),
                "metadata": {
                    "patientName": str(dcm.PatientName),
                    "patientID": str(dcm.PatientID),
                    "patientBirthDate": datetime.strptime(str(dcm.PatientBirthDate), '%Y%m%d') if dcm.PatientBirthDate else None,
                    "patientSex": str(dcm.PatientSex),
                    "patientAge": str(dcm.PatientAge) if hasattr(dcm, 'PatientAge') else None,
                    "studyDescription": str(dcm.StudyDescription),
                    "studyDate": datetime.strptime(str(dcm.StudyDate), '%Y%m%d') if dcm.StudyDate else None,
                    "studyInstanceUID": str(dcm.StudyInstanceUID),
                    "seriesDescription": str(dcm.SeriesDescription),
                    "seriesInstanceUID": str(dcm.SeriesInstanceUID),
                    "seriesNumber": str(dcm.SeriesNumber),
                    "modality": str(dcm.Modality),
                    "instanceNumber": str(dcm.InstanceNumber),
                    "sopInstanceUID": str(dcm.SOPInstanceUID),
                    "physicianName": str(dcm.PhysiciansName) if dcm.get("PhysiciansName") else '',
                    "imageType": [str(val) for val in dcm.ImageType] if dcm.get("ImageType") else [],
                },
            }
            # Save the DICOM file to disk
            dcm.save_as(metadata["filepath"])
            return metadata
        except Exception as e:
            # Handle any exceptions here (e.g., invalid DICOM format)
            print(f"Error extracting metadata from DICOM: {str(e)}")
            return None

    @staticmethod
    def serialize_file(file):
        """Serialize file object"""
        return {
            "id": str(file['_id']),
            "filename": file['filename'],
            "uploadDate": file['uploadDate'].isoformat(),
            "metadata": file['metadata'],
            "uploader_id": file['uploader_id'],
        }
