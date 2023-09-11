from dotenv import load_dotenv
from os import getenv


load_dotenv()

MYSQL_HOST = getenv('MYSQL_HOST', '')
MYSQL_PORT = int(getenv('MYSQL_PORT', '3306'))
MYSQL_USER = getenv('MYSQL_USER', '')
MYSQL_PASSWORD = getenv('MYSQL_PASSWORD', '')
MYSQL_DB = getenv('MYSQL_DB', '')


class Config:
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
