from flask import Blueprint, request, render_template

from ..models import Customer, Shop

shop = Blueprint('shop', __name__)

@shop.route('/shop')
def shop_list():
    page = request.args.get('page', 1, type=int)


    shops = Shop.query.paginate(page=page, per_page=20)
    count = len(Shop.query.all())

    return render_template('shop.html', shops=shops, count=count)

