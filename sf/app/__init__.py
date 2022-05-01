from flask import Flask

from .extentions import db
from .views import top

from .contractor.views import contractor

def create_app():
    app = Flask(__name__)

    if app.config['ENV'] == 'production':
        app.config.from_object('app.config.ProductionConfig')
    
    elif app.config['ENV'] == 'testing':
        app.config.from_object('app.config.TestingConfig')

    else:
        app.config.from_object('app.config.DevelopmentConfig')

    db.init_app(app)

    app.register_blueprint(top)
    app.register_blueprint(contractor)

    return app
