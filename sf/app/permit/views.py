from flask import Blueprint, render_template

from ..utils import get_contractor

from .forms import PermitRegisterForm

permit = Blueprint('permit', __name__, url_prefix='/permit')

@permit.route('/')
def index():

    return 'パーミット'


@permit.route('/register/<int:contractor_id>')
def register(contractor_id):

    contractor = get_contractor(contractor_id)
    form = PermitRegisterForm()

    return render_template('permit/register.html', contractor=contractor, form=form)


@permit.route('/<int:contractor_id>/<int:id>')
def details(contractor_id, id, mode=None):
    return render_template('permit/details.html')