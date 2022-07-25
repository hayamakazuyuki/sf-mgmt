from flask import Flask

from .extentions import oauth
from .views import view

def create_app():
    app = Flask(__name__)

    if app.config['ENV'] == 'production':
        app.config.from_object('app.config.ProductionConfig')

    elif app.config['ENV'] == 'testing':
        app.config.from_object('app.config.TestingConfig')

    else:
        app.config.from_object('app.config.DevelopmentConfig')
    
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

    app.register_blueprint(view)

    return app
