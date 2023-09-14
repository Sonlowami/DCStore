from os import getenv
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# MongoDB configuration
MONGO_HOST = getenv('MONGO_HOST', 'localhost')
MONGO_PORT = getenv('MONGO_PORT', 27017)
MONGO_DBNAME = getenv('MONGO_DBNAME', '')


class Config:
    """Base configuration"""
    DEBUG = getenv('DEBUG', False)
    MONGO_URI = f'mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DBNAME}'
