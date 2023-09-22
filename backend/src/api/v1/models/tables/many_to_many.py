from api.v1.utils.database import db


# Define many to many relationship between users and patients
user_patient = db.Table(
    'user_patient',
    db.Column('user_id', db.String(80), db.ForeignKey('users.id'), primary_key=True),
    db.Column('patient_id', db.String(80), db.ForeignKey('patients.id'), primary_key=True)
)

# Define many to many relationship between users and studies
user_study = db.Table(
    'user_study',
    db.Column('user_id', db.String(80), db.ForeignKey('users.id'), primary_key=True),
    db.Column('study_id', db.String(80), db.ForeignKey('studies.id'), primary_key=True)
)

# Define many to many relationship between users and series
user_series = db.Table(
    'user_series',
    db.Column('user_id', db.String(80), db.ForeignKey('users.id'), primary_key=True),
    db.Column('series_id', db.String(80), db.ForeignKey('series.id'), primary_key=True)
)

# Define many to many relationship between users and instances
user_instance = db.Table(
    'user_instance',
    db.Column('user_id', db.String(80), db.ForeignKey('users.id'), primary_key=True),
    db.Column('instance_id', db.String(80), db.ForeignKey('instances.id'), primary_key=True)
)
