from flask import Flask
from .extentions import db, oauth

from app.main import main
from app.auth import auth
from app.shop import shop
from app.contractor import contractor
from app.contract import contract
from .license import license
from .permit import permit


def create_app():
    app = Flask(__name__)

    if app.config['ENV'] == 'production':
        app.config.from_object('app.config.ProductionConfig')

    elif app.config['ENV'] == 'testing':
        app.config.from_object('app.config.TestingConfig')

    else:
        app.config.from_object('app.config.DevelopmentConfig')

    db.init_app(app)

    oauth.init_app(app)

    oauth.register(
        "auth0",
        client_id=app.config["AUTH0_CLIENT_ID"],
        client_secret=app.config["AUTH0_CLIENT_SECRET"],
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f'https://{app.config["AUTH0_DOMAIN"]}/.well-known/openid-configuration'
    )

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(shop)
    app.register_blueprint(contractor)
    app.register_blueprint(contract)
    app.register_blueprint(license)
    app.register_blueprint(permit)
    
    return app
