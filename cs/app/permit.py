from flask import Blueprint, render_template
from .models import Permit

permit = Blueprint('permit', __name__, url_prefix='/permit')


# permit details
@permit.route('/<int:id>')
def details(id):
    permit = Permit.query.get(id)

    return render_template('permit/permit-details.html', permit=permit)
