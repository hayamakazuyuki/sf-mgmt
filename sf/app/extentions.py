from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from google.cloud import storage

db = SQLAlchemy()
admin = Admin(template_mode='bootstrap4')
storage = storage
