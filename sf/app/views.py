from flask import Blueprint, render_template

top = Blueprint('top', __name__)

@top.route('/')
def index():
    return render_template('index.html')

@top.route('/komeri')
def komeri():
    return render_template('komeri.html')

@top.route('/terms')
def terms():
    return render_template('terms.html')
