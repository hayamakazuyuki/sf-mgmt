from flask import Blueprint, render_template, request

from ..models import Contractor

contractor = Blueprint('contractor', __name__)

@contractor.route('/contractor')
def index():
    
    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)

    if q:

        search = "%{}%".format(q)
        contractors = Contractor.query.filter(Contractor.name.like(search)).paginate(page=page, per_page=20)

        return render_template('contractor/index.html', page=page, contractors=contractors)

    else:
        contractors = Contractor.query.paginate(page=page, per_page=20)

        return render_template('contractor/index.html', page=page, contractors=contractors)


@contractor.route('/contractor/<int:id>')
def contractor_profile(id):

    contractor = Contractor.query.get_or_404(id)
    
    return render_template('contractor/profile.html', contractor=contractor)
