from flask import Blueprint, render_template, request, flash, redirect, url_for

from ..extentions import db

from ..models import Customer

from .forms import CustomerForm

customer = Blueprint('customer', __name__, url_prefix='/customer')

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
@customer.route('/<int:id>/<mode>')
def profile(id, mode=None):
    customer = Customer.query.get(id)

    if mode == 'edit':
        return '編集'

    return render_template('customer/profile.html', customer=customer)
