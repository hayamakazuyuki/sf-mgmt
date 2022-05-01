from flask import Blueprint, render_template

top = Blueprint('top', __name__)

@top.route('/')
def index():
    return render_template('index.html')
    