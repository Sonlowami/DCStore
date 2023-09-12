from dotenv import load_dotenv
from os import getenv


load_dotenv()

# Database configuration
MYSQL_HOST = getenv('MYSQL_HOST', '')
MYSQL_PORT = int(getenv('MYSQL_PORT', '3306'))
MYSQL_USER = getenv('MYSQL_USER', '')
MYSQL_PASSWORD = getenv('MYSQL_PASSWORD', '')
MYSQL_DB = getenv('MYSQL_DB', '')

# Mail configuration
MAIL_SERVER = getenv('MAIL_SERVER', '')
MAIL_PORT = int(getenv('MAIL_PORT', '465'))
MAIL_USERNAME = getenv('MAIL_USERNAME', '')
MAIL_PASSWORD = getenv('MAIL_PASSWORD', '')
MAIL_USE_TLS = getenv('MAIL_USE_TLS', 'true').lower() == 'true'
MAIL_USE_SSL = getenv('MAIL_USE_SSL', 'false').lower() == 'true'


class Config:
    SECRET_KEY = getenv('SECRET_KEY', '')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = MAIL_SERVER
    MAIL_PORT = MAIL_PORT
    MAIL_USERNAME = MAIL_USERNAME
    MAIL_PASSWORD = MAIL_PASSWORD
    MAIL_USE_TLS = MAIL_USE_TLS
    MAIL_USE_SSL = MAIL_USE_SSL
    SWAGGER = {'title': 'DCStore API Documentation', 'uiversion': 3}

