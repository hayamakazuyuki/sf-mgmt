from flask import Blueprint, session, render_template
from datetime import timedelta, timezone, datetime

from ..extentions import db

from ..models import Customer, Shop, ContractShop, VolumeReport

customer = Blueprint('customer', __name__)
JST = timezone(timedelta(hours=+9), 'JST')

@customer.route('/shop/<int:id>')
def shop_profile(id):

    customer_id = session['profile']['customer_id']
    shop = Shop.query.get((customer_id, id))
    
    contracts = ContractShop.query.filter_by(customer_id=customer_id).filter_by(shop_id=id).all()

    reports = VolumeReport.query.filter(VolumeReport.customer_id == customer_id).all()

    today = datetime.now(JST).date()

    return render_template('customer/shop-profile.html', shop=shop, contracts=contracts, reports=reports, today=today)



