import os

class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@mysql_c/devdb?charset=utf8'
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME')

    AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
    AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
    SECRET_KEY = os.environ.get('SECRET_KEY')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


class TestingConfig(BaseConfig):
    TESTING =True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    GCS_BUCKET_NAME = 'GCS_BUCKET_NAME'
