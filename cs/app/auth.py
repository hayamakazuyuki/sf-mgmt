import json
from flask import Blueprint, url_for, session, redirect, current_app, render_template
from urllib.parse import quote_plus, urlencode
from functools import wraps

from .extentions import oauth


auth = Blueprint('auth', __name__)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated


@auth.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for('auth.callback', _external=True)
    )


@auth.route("/callback", methods=["GET", "POST"])
def callback():

    token = oauth.auth0.authorize_access_token()
    session['user'] = token

    session['profile'] = {
        'uuid' : token['userinfo']['https://app.singen.io/claims/uuid'],
        'customer_id' : token['userinfo']['https://app.singen.io/claims/customerid'],
        'name' : token['userinfo']['name']
    }
    
    return redirect(url_for('main.home'))


@auth.route("/logout")
@requires_auth
def logout():
    session.clear()
    return redirect(
        "https://" + current_app.config["AUTH0_DOMAIN"]
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": "https://www.singen.io/",
                "client_id": current_app.config["AUTH0_CLIENT_ID"],
            },
            quote_via=quote_plus,
        )
    )

# @auth.route('/info')
# @requires_auth
# def info():

#     return render_template("info.html", session=session['user'], pretty=json.dumps(session['user'], indent=4))

