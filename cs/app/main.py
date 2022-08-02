from flask import Blueprint, session, render_template, request

from .models import Customer, Shop, VolumeReport

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if 'user' in session:

        userinfo = session['user']['userinfo']

        hq = userinfo.get('hq')
        customer_id = userinfo.get('customer')
        shop_id = userinfo.get('shop')

        page = request.args.get('page', 1, type=int)

        if hq:
            customers = Customer.query.filter(Customer.parent_id == hq).all()

            shops = Shop.query.filter(Shop.customer_id.in_([c.id for c in customers])).paginate(page=page, per_page=20)

            count = len(Shop.query.filter(Shop.customer_id.in_([c.id for c in customers])).all())

            return render_template('home.html', shops=shops, count=count)

        elif customer_id and shop_id is None:
            shops = Shop.query.paginate(page=page, per_page=20)
            count = len(Shop.query.all())

        else: 
            shop = Shop.query.get((customer_id, shop_id))
            reports = VolumeReport.query.all()

            return render_template('home-shop.html', shop=shop, reports=reports)

    else:

        return render_template('index.html')


@main.route('/session')
def show_session():
    show = session.get('user').get('userinfo').get('customer')

    return show