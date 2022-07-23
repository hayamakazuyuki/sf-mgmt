from flask import Flask

from .views import view

def create_app():
    app = Flask(__name__)

    app.register_blueprint(view)
    
    return app
