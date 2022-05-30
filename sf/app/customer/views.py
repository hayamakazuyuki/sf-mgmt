from flask import Blueprint, render_template, request, flash, redirect, url_for

from ..extentions import db

from ..models import Customer, Shop, Parent

from .forms import CustomerForm, ShopForm

customer = Blueprint('customer', __name__, url_prefix='/customer')


@customer.route('/parent')
def parent():
    parents = Parent.query.all()

    return render_template('customer/parent.html', parents=parents)


@customer.route('/')
def index():

    q = request.args.get('q')

    if q:
        search = "%{}%".format(q)
        page = request.args.get('page', 1, type=int)
        customers = Customer.query.filter(Customer.name.like(search)).paginate(page=page, per_page=20)
        count = len(Customer.query.filter(Customer.name.like(search)).all())

        return render_template('customer/index.html', page=page, customers=customers, count=count, search=search)
    
    else:
        return render_template('customer/index.html')

@customer.route('/register', methods=['GET', 'POST'])
def register():
    form = CustomerForm()

    if form.validate_on_submit():
        id = request.form['id']
        
        # check if id already exists in the db
        exists = Customer.query.get(id)

        if exists:
            return 'あります'

        else:
            name = request.form['name']
            title = request.form.get('title')
            representative = request.form['representative']
            zip = request.form['zip']
            prefecture = request.form['prefecture']
            city = request.form['city']
            town = request.form['town']
            address = request.form.get('address')
            bldg = request.form.get('bldg')
            registered_by = 1

            customer = Customer(id=id, name=name, title=title, representative=representative, zip=zip,
             prefecture=prefecture, city=city, town=town, address=address, bldg=bldg, registered_by=registered_by)

            db.session.add(customer)
            
            db.session.commit()

            flash('取引先を登録しました。', 'success')

            return redirect(url_for('customer.profile', id=id))

    return render_template('customer/register.html', form=form)


# show and update customer profile
@customer.route('/<int:id>')
@customer.route('/<int:id>/<mode>', methods=['GET', 'POST'])
def profile(id, mode=None):
    customer = Customer.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)

    shops = Shop.query.filter_by(customer_id=id).paginate(page=page, per_page=20)

    if mode == 'edit':
        form = CustomerForm()

        if form.validate_on_submit():
            customer.name = request.form['name']
            customer.title = request.form.get('title')
            customer.representative = request.form['representative']
            customer.zip = request.form['zip']
            customer.prefecture = request.form['prefecture']
            customer.city = request.form['city']
            customer.town = request.form['town']
            customer.address = request.form.get('address')
            customer.bldg = request.form.get('bldg')
            customer.registered_by = 1

            db.session.commit()

            flash('取引先の情報を更新しました。')

            return redirect(url_for('customer.profile', id=id))

        return render_template('customer/edit.html', form=form, customer=customer)

    return render_template('customer/profile.html', customer=customer, shops=shops)


@customer.route('/<int:id>/register', methods=['GET', 'POST'])
def shop_register(id):
    form = ShopForm()
    customer = Customer.query.get(id)

    if form.validate_on_submit():
        # has to check if the id already exists in the Shop table
        customer_id = customer.id
        shop_id = request.form['id']
        shop_number = request.form.get('shop_number')
        name = request.form['name']
        zip = request.form['zip']
        prefecture = request.form['prefecture']
        city = request.form['city']
        town = request.form['town']
        address = request.form.get('address')
        bldg = request.form.get('bldg')
        registered_by = 1

        # check if requested shop already exists in the db
        exists = Shop.query.get((customer_id, shop_id))

        if exists:
            return redirect(url_for('customer.shop_profile', customer_id=customer_id, id=shop_id))

        else:

            shop = Shop(customer_id=customer_id, id=shop_id, shop_number=shop_number, name=name, zip=zip,
                 prefecture=prefecture, city=city, town=town, address=address, bldg=bldg, registered_by=registered_by)

            db.session.add(shop)
    
            db.session.commit()

            flash('事業所を登録しました。', 'success')

            return redirect(url_for('customer.shop_profile', customer_id=customer_id, id=shop_id))

    return render_template('customer/shop-register.html', customer=customer, form=form)


# show and update shop profile
@customer.route('/<int:customer_id>/<int:id>')
@customer.route('/<int:customer_id>/<int:id>/<mode>', methods=['GET', 'POST'])
def shop_profile(customer_id, id, mode=None):
    shop = Shop.query.get_or_404((customer_id, id))

    if mode == 'edit':
        form = ShopForm()

        if form.validate_on_submit():
            shop.shop_number = request.form.get('shop_number')
            shop.name = request.form['name']
            shop.zip = request.form['zip']
            shop.prefecture = request.form['prefecture']
            shop.city = request.form['city']
            shop.town = request.form['town']
            shop.address = request.form.get('address')
            shop.bldg = request.form.get('bldg')
            shop.registered_by = 1

            db.session.commit()

            flash('事業所の情報を更新しました。')

            return redirect(url_for('customer.shop-profile', customer_id=customer_id, id=id))

        return render_template('customer/shop-edit.html', shop=shop, form=form)

    return render_template('customer/shop-profile.html', shop=shop)

