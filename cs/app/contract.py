from flask import Blueprint, render_template, request

from .models import Contract, Shop

contract = Blueprint('contract', __name__)

@contract.route('/contract/<int:id>')
def contract_details(id):

    contract = Contract.query.get(id)
    shop = Shop.query.get((contract.customer_id, contract.shop_id))

    return render_template('contract/contract-details.html', contract=contract, shop=shop)
    