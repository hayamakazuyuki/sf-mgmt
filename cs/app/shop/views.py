from flask import Blueprint, render_template

from ..models import Shop

shop = Blueprint('shop', __name__)


@shop.route('/<int:id>')
def shop_profile(id):
    shop = Shop.query.get((99999, id))
    return render_template('shop/shop-profile.html', shop=shop)
