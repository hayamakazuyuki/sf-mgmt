from flask import Blueprint, session, render_template, request, redirect, url_for

from .models import Shop, Contractor

main = Blueprint('main', __name__)


@main.route('/')
def home():
    if 'profile' in session:

        customer_id = session['profile']['customer_id']
        shops_count = len(Shop.query.filter(Shop.customer_id==customer_id).all())
        contractors_count = len(Contractor.query.filter(Contractor.contracts.any(customer_id=customer_id)).all())

        return render_template('customer/home.html', shops_count=shops_count, contractors_count=contractors_count)

    else:
        return redirect(url_for('auth.login'))

# @main.route('/')
# def index():

#     page = request.args.get('page', 1, type=int)

#     if 'user' in session:

        # userinfo = session['user']['userinfo']

        # hq = userinfo.get('hq')
        # customer_id = userinfo.get('customer')
        # shop_id = userinfo.get('shop')

        # page = request.args.get('page', 1, type=int)

        # if hq:
        #     customers = Customer.query.filter(Customer.parent_id == hq).all()

        #     shops = Shop.query.filter(Shop.customer_id.in_([c.id for c in customers])).paginate(page=page, per_page=20)

        #     count = len(Shop.query.filter(Shop.customer_id.in_([c.id for c in customers])).all())

        #     return render_template('home.html', shops=shops, count=count)

        # elif customer_id and shop_id is None:

        # return redirect(url_for('shop.index'))

        # else:

        #     return redirect(url_for('shop.shop_profile', id=shop_id))

    # else:

    #     return render_template('index.html')
