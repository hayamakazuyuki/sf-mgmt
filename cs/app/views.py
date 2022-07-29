import json
from functools import wraps
from flask import Blueprint, redirect, render_template, current_app, url_for, session
from urllib.parse import quote_plus, urlencode


from .extentions import oauth

view = Blueprint('view', __name__)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated




@view.route('/info')
@requires_auth
def info():
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))


@view.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for('view.callback', _external=True)
    )


@view.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect(url_for('main.index'))


@view.route("/logout")
@requires_auth
def logout():
    session.clear()
    return redirect(
        "https://" + current_app.config["AUTH0_DOMAIN"]
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("main.index", _external=True),
                "client_id": current_app.config["AUTH0_CLIENT_ID"],
            },
            quote_via=quote_plus,
        )
    )
