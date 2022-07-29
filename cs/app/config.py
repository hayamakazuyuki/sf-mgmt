from os import environ as env
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()

if ENV_FILE:
    load_dotenv(ENV_FILE)

class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@mysql_c/devdb?charset=utf8'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    SECRET_KEY = env.get('SECRET_KEY')

    GCS_BUCKET_NAME = env.get('GCS_BUCKET_NAME')
    AUTH0_CLIENT_ID = env.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = env.get('AUTH0_CLIENT_SECRET')
    AUTH0_DOMAIN = env.get('AUTH0_DOMAIN')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = env.get('SQLALCHEMY_DATABASE_URI')


class TestingConfig(BaseConfig):
    TESTING =True


class DevelopmentConfig(BaseConfig):
    DEBUG = True
