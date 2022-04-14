from flask import Blueprint, render_template

contractor = Blueprint('contractor', __name__)

@contractor.route('/')
def index():
    return render_template('index.html')


@contractor.route('/register')
def register():
    return render_template('contractor/register.html')