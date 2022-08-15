import os
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()

if ENV_FILE:
    load_dotenv(ENV_FILE)


class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@mysql_c/devdb?charset=utf8'
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME')
    X_API_KEY = os.environ.get('X_API_KEY')
    JSON_AS_ASCII = False


class ProductionConfig(BaseConfig):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


class TestingConfig(BaseConfig):
    TESTING =True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    GCS_BUCKET_NAME = 'GCS_BUCKET_NAME'
