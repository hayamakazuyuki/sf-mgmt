from flask import Blueprint, render_template, request

from .models import Shop

shop = Blueprint('shop', __name__)


@shop.route('/shop')
def find_shop():

    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)

    if q:

        search = "%{}%".format(q)
        shops = Shop.query.filter(Shop.name.like(search)).paginate(page=page, per_page=20)
        count = len(Shop.query.filter(Shop.name.like(search)).all())

        return render_template('home.html', page=page, shops=shops, count=count)

    else:
        shops = Shop.query.paginate(page=page, per_page=20)
        
        count = len(Shop.query.all())

        return render_template('home.html', page=page, shops=shops, count=count)


@shop.route('/<int:id>')
def shop_profile(id):
    shop = Shop.query.get((99999, id))
    return render_template('shop/shop-profile.html', shop=shop)
