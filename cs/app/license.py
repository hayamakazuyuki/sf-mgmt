from flask import Blueprint, render_template
from .models import License

license = Blueprint('license', __name__, url_prefix='/license')


# license details
@license.route('/<int:id>')
def details(id):
    license = License.query.get(id)

    return render_template('license/license-details.html', license=license)
