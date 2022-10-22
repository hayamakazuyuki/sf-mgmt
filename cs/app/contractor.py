from flask import Blueprint, render_template, request
from datetime import datetime, timedelta, timezone

from .models import Contractor, License, Permit

contractor = Blueprint('contractor', __name__)
JST = timezone(timedelta(hours=+9), 'JST')


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

    permits = Permit.query.filter(Permit.contractor_id == id).all()
    licenses = License.query.filter(License.contractor_id == id).all()
    today = datetime.now(JST).date()

    return render_template('contractor/profile.html', contractor=contractor, permits=permits, licenses=licenses, today=today)


@contractor.route('/contractor/<int:contractor_id>/permit/<int:id>')
def permit_details(contractor_id, id):
    
    contractor = Contractor.query.get(contractor_id)
    permit = Permit.query.get(id)

    return render_template('contractor/permit-details.html', contractor=contractor, permit=permit)
