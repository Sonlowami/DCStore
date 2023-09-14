from flask import redirect, request, jsonify

from api.v1.models import File, User, Study, Series, Patient, Instance
from api.v1.views.auth.decorator import authorize
from api.v1.auth.helpers import getuser
from api.v1.views import app_views

import pydicom

@app_views.post('/upload')
@authorize
def upload_dicom(email: str) -> str:
    """Allow a user to upload one or more dicom files
    The user must be authenticated with a JWT, and all uploaded files
    should be with a .dcm extension"""
    user: User = getuser(email)
    files = request.files

