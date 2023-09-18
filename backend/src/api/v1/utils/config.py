from dotenv import load_dotenv
from os import getenv


load_dotenv()

# MongoDB configuration
MONGO_HOST = getenv('MONGO_HOST', 'localhost')
MONGO_PORT = int(getenv('MONGO_PORT', '27017'))
MONGO_DBNAME = getenv('MONGO_DBNAME', 'dcstore')

# MySQL configuration
MYSQL_HOST = getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = getenv('MYSQL_USER', '')
MYSQL_PASSWORD = getenv('MYSQL_PASSWORD', '')
MYSQL_DB = getenv('MYSQL_DB', '')
MYSQL_PORT = getenv('MYSQL_PORT', '3306')

# Mail configuration
MAIL_SERVER = getenv('MAIL_SERVER', '')
MAIL_PORT = int(getenv('MAIL_PORT', '465'))
MAIL_USERNAME = getenv('MAIL_USERNAME', '')
MAIL_PASSWORD = getenv('MAIL_PASSWORD', '')
MAIL_USE_TLS = getenv('MAIL_USE_TLS', 'true').lower() == 'true'
MAIL_USE_SSL = getenv('MAIL_USE_SSL', 'false').lower() == 'true'

# redis configuration
REDIS_HOST = getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(getenv('REDIS_PORT', '6379'))
REDIS_DB = int(getenv('REDIS_DB', '0'))


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
    REDIS_URI = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
