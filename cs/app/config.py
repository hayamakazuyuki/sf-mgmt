import os

class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@mysql_c/devdb?charset=utf8'
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME')
    AUTH0_CLIENT_ID = 'zTxpKt2O3PSy8P6dPPxXBFwlgYYwwdYJ'
    AUTH0_CLIENT_SECRET = 'ygNVxABkZEM302tZzAPmNF-N8zqWrmjiw5B-SyJwoMcLy3FmwLNIrhYi9ORDNOA4'
    AUTH0_DOMAIN = 'singen-dev.jp.auth0.com'

class ProductionConfig(BaseConfig):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


class TestingConfig(BaseConfig):
    TESTING =True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    GCS_BUCKET_NAME = 'GCS_BUCKET_NAME'
