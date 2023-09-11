from api.v1.utils.database import db
from api.v1.app import app
from api.v1.models.patient import Patient
from api.v1.models.study import Study
from api.v1.models.series import Series
from api.v1.models.instance import Instance
from api.v1.models.file import File
from api.v1.models.user import User

import uuid

# Create user
user = User(
    id=str(uuid.uuid4()),
    first_name='Evan',
    last_name='Harris',
    email='evan@mail.com',
    password_hash='password',
    role='physician',
)

# Create patient
patient = Patient(
    id=str(uuid.uuid4()),
    name='John Doe',
    birth_date='1990-01-01',
    sex='Male',
)

# Create study
study = Study(
    id=str(uuid.uuid4()),
    patient_id=patient.id,
    date='2020-01-01',
    physician='Dr. Smith',
    description='This is a study',
)

# Create series
series = Series(
    id=str(uuid.uuid4()),
    study_id=study.id,
    modality='CT',
    description='This is a series',
)

# Create instance
instance = Instance(
    id=str(uuid.uuid4()),
    series_id=series.id,
    content_datetime='2020-01-01 00:00:00',
    description='This is an instance',
)

# Create file
file = File(
    id=str(uuid.uuid4()),
    instance_id=instance.id,
    path='/path/to/file.dcm',
    size=1024,
    md5='d41d8cd98f00b204e9800998ecf8427e',
    owner_id=user.id,
)

print(f'insance id: {instance.id}')
print(f'file insance id: {file.instance_id}')

print(instance.id == file.instance_id)

# Add and commit
with app.app_context():
    db.session.add(user)
    db.session.add(patient)
    db.session.add(study)
    db.session.add(series)
    db.session.add(instance)
    db.session.commit()
    db.session.add(file)
    db.session.commit()


