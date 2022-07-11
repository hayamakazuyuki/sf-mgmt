import os

class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@mysql_c/devdb?charset=utf8'
    GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME')


class ProductionConfig(BaseConfig):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


class TestingConfig(BaseConfig):
    TESTING =True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    GCS_BUCKET_NAME = 'GCS_BUCKET_NAME'
