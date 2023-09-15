from dotenv import load_dotenv
from os import getenv


load_dotenv()

# Database configuration
MONGO_HOST = getenv('MONGO_HOST', 'localhost')
MONGO_PORT = int(getenv('MONGO_PORT', '27017'))
MONGO_DBNAME = getenv('MONGO_DBNAME', 'dcstore')

# Mail configuration
MAIL_SERVER = getenv('MAIL_SERVER', '')
MAIL_PORT = int(getenv('MAIL_PORT', '465'))
MAIL_USERNAME = getenv('MAIL_USERNAME', '')
MAIL_PASSWORD = getenv('MAIL_PASSWORD', '')
MAIL_USE_TLS = getenv('MAIL_USE_TLS', 'true').lower() == 'true'
MAIL_USE_SSL = getenv('MAIL_USE_SSL', 'false').lower() == 'true'


class Config:
    SECRET_KEY = getenv('SECRET_KEY', '')
    MAIL_SERVER = MAIL_SERVER
    MAIL_PORT = MAIL_PORT
    MAIL_USERNAME = MAIL_USERNAME
    MAIL_PASSWORD = MAIL_PASSWORD
    MAIL_USE_TLS = MAIL_USE_TLS
    MAIL_USE_SSL = MAIL_USE_SSL
    SWAGGER = {'title': 'DCStore API Documentation', 'uiversion': 3}
    DEBUG = getenv('DEBUG', False)
    MONGO_URI = f'mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DBNAME}'
