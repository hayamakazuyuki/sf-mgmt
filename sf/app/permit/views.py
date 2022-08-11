from crypt import methods
from flask import Blueprint, render_template

from ..utils import get_contractor

from .forms import PermitRegisterForm

permit = Blueprint('permit', __name__, url_prefix='/permit')


@permit.route('/register/<int:contractor_id>')
def register(contractor_id):

    contractor = get_contractor(contractor_id)
    form = PermitRegisterForm()

    return render_template('permit/register.html', contractor=contractor, form=form)


@permit.route('/<int:contractor_id>/<int:id>')
@permit.route('/<int:contractor_id>/<int:id>/<mode>', methods=['GET', 'POST'])
def details(contractor_id, id, mode=None):
    
    contractor = get_contractor(contractor_id)

    if mode == 'edit':
        return '編集'

    return render_template('permit/details.html', contractor=contractor)