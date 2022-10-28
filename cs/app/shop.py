from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from datetime import datetime, timedelta, timezone
from sqlalchemy import desc

from .extentions import db
from .models import Customer, CollectionRequest, Contract, Shop, VolumeReport
from .forms import CollectionRequestForm


shop = Blueprint('shop', __name__, url_prefix='/shop')
JST = timezone(timedelta(hours=+9), 'JST')

@shop.route('/')
def index():

    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)

    customer_id = session['profile']['customer_id']

    if q:

        search = "%{}%".format(q)
        shops = Shop.query.filter(Shop.customer_id == customer_id).filter(Shop.name.like(search)).paginate(page=page, per_page=20)
        count = len(Shop.query.filter(Shop.customer_id == customer_id).filter(Shop.name.like(search)).all())

        return render_template('shop/shop.html', page=page, shops=shops, count=count)

    else:
        shops = Shop.query.filter(Shop.customer_id == customer_id).paginate(page=page, per_page=20)
        
        count = len(Shop.query.filter(Shop.customer_id == customer_id).all())

        return render_template('shop/shop.html', page=page, shops=shops, count=count)

"""
@shop.route('/collection')
def collection():

    userinfo = session['user']['userinfo']
    hq = userinfo.get('hq')

    if hq:
        customers = Customer.query.filter(Customer.parent_id == hq).all()

        # shops = Shop.query.filter(Shop.customer_id.in_([c.id for c in customers])).paginate(page=page, per_page=20)

        requests = CollectionRequest.query.filter(CollectionRequest.customer_id.in_([c.id for c in customers])).order_by(desc(CollectionRequest.id)).all()
    
        return render_template('shop/collection.html', requests=requests)

    else:

        customer_id = session['user']['userinfo'].get('customer')
        shop_id = session['user']['userinfo'].get('shop')

        requests = CollectionRequest.query.filter_by(customer_id=customer_id).filter_by(shop_id=shop_id).order_by(desc(CollectionRequest.id)).all()
    
        return render_template('shop/collection.html', requests=requests)


@shop.route('/collection-request', methods=['GET', 'POST'])
def collection_request():

    customer_id = session['user']['userinfo'].get('customer')
    shop_id = session['user']['userinfo'].get('shop')

    shop = Shop.query.get((customer_id, shop_id))

    form = CollectionRequestForm()

    if form.validate_on_submit():

        customer_id = customer_id
        shop_id = shop_id
        details = request.form['details']
        preferreddate = request.form.get('preferreddate')
        fluorescentlamp = request.form.get('fluorescentlamp')
        battery = request.form.get('battery')
        consumerelectronics = request.form.get('consumerelectronics')
        registered_by = session['user']['userinfo']['email']

        cr = CollectionRequest(customer_id=customer_id, shop_id=shop_id, details=details, preferreddate=preferreddate,
            fluorescentlamp=fluorescentlamp, battery=battery, consumerelectronics=consumerelectronics, registered_by=registered_by)

        db.session.add(cr)
        db.session.commit()
        
        flash('新規の産廃処理依頼を受け付けました。', 'success')

        return redirect(url_for('shop.collection'))

    return render_template('shop/collection-request.html', shop=shop, form=form)

"""