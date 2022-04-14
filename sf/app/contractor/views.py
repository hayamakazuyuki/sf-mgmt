from flask import Blueprint

contractor = Blueprint('contractor', __name__)

@contractor.route('/')
def index():
    return 'これ'