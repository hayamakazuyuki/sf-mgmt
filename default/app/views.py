from flask import Blueprint, render_template, url_for, redirect, session, current_app
from urllib.parse import quote_plus, urlencode

from .extentions import oauth

view = Blueprint('view', __name__)


@view.route('/')
def index():
    return render_template('index.html')

@view.route('/home')
def home():
    return 'インデックス'


@view.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for('view.callback', _external=True)
    )


@view.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect(url_for('view.home'))


@view.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + current_app.config["AUTH0_DOMAIN"]
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("view.index", _external=True),
                "client_id": current_app.config["AUTH0_CLIENT_ID"],
            },
            quote_via=quote_plus,
        )
    )