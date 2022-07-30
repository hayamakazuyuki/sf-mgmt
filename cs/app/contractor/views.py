from flask import Blueprint, render_template, request

from ..models import Contractor

contractor = Blueprint('contractor', __name__)

@contractor.route('/contractor')
def index():
    
    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)

    if q:
        return 'q'

    else:
        contractors = Contractor.query.paginate(page=page, per_page=20)

        return render_template('contractor/index.html', page=page, contractors=contractors)


"""
    if q:
        search = "%{}%".format(q)
        page = request.args.get('page', 1, type=int)
        customers = Customer.query.filter(Customer.name.like(search)).paginate(page=page, per_page=20)
        count = len(Customer.query.filter(Customer.name.like(search)).all())

        return render_template('customer/index.html', page=page, customers=customers, count=count, search=search)
"""
