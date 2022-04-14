from flask import Flask

from .contractor.views import contractor

def create_app():
    app = Flask(__name__)

    app.register_blueprint(contractor)

    return app
