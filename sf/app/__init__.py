from flask import Flask

from .extentions import db, admin
from .views import top

from .contract.views import contract
from .contractor.views import contractor
from .customer.views import customer
from .report.views import report
from .license.views import license
from .permit.views import permit


def create_app():
    app = Flask(__name__)

    if app.config['ENV'] == 'production':
        app.config.from_object('app.config.ProductionConfig')

    elif app.config['ENV'] == 'testing':
        app.config.from_object('app.config.TestingConfig')

    else:
        app.config.from_object('app.config.DevelopmentConfig')

    db.init_app(app)
    admin.init_app(app)

    app.register_blueprint(top)
    app.register_blueprint(contract)
    app.register_blueprint(customer)
    app.register_blueprint(contractor)
    app.register_blueprint(report)
    app.register_blueprint(license)
    app.register_blueprint(permit)

    return app
