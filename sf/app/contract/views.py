from flask import Blueprint, render_template, request, redirect, url_for

from ..extentions import db

from ..models import Contract, Shop
from .forms import ContractRegisterForm


contract = Blueprint('contract', __name__, url_prefix='/contract')


@contract.route('/')
def index():
    return render_template('contract/index.html')


@contract.route('/register/<int:customer_id>/<int:id>', methods=['GET', 'POST'])
def register(customer_id, id):

    shop = Shop.query.get_or_404((customer_id, id))
    form = ContractRegisterForm()

    if form.validate_on_submit():
        customer_id = request.form['customer_id']
        shop_id = request.form['shop_id']
        contractor_id = request.form['contractor_id']
        item_id = request.form['item_id']
        registered_by = 1

        new_contract = Contract(customer_id= customer_id, shop_id=shop_id, contractor_id=contractor_id,
            item_id=item_id, registered_by=registered_by)

        db.session.add(new_contract)
        db.session.commit()

        return redirect(url_for('customer.shop_profile', customer_id=customer_id, id=shop_id))

    return render_template('contract/register.html', shop=shop, form=form)
