from flask import Blueprint, render_template, current_app

view = Blueprint('view', __name__)

@view.route('/')
def index():
    debug = current_app.config['DEBUG']
    gcs = current_app.config['GCS_BUCKET_NAME']
    return render_template('index.html', gcs=gcs)

@view.route('/home')
def home():
    return render_template('home.html')
