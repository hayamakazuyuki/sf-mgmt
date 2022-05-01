from email.policy import default
from flask import Blueprint, render_template, request, flash, redirect, url_for

from ..extentions import db

from ..models import Contractor, Satiscare

from .forms import ContractorForm

contractor = Blueprint('contractor', __name__)

@contractor.route('/contractor')
def index():

    q = request.args.get('q', default=None)

    if q:
        page = request.args.get('page', 1, type=int)

        if q.isdigit():
            contractor = Contractor.query.get(q)

            if contractor:
                return redirect(url_for('contractor.profile', id=q))

            else:
                return redirect(url_for('contractor.index'))

        else:
            search = "%{}%".format(q)
            contractors = Contractor.query.filter(Contractor.name.like(search)).paginate(page=page, per_page=20)
            count = len(Contractor.query.filter(Contractor.name.like(search)).all())

            return render_template('contractor/index.html', page=page, contractors=contractors, count=count)
    else:
        return render_template('contractor/index.html')


@contractor.route('/contractor/register', methods=['GET', 'POST'])
def register():

    form = ContractorForm()

    if form.validate_on_submit():

        id = request.form['id']
        
        # check if id already exists in the db
        exists = Contractor.query.get(id)

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
            tel = request.form['tel']
            registered_by = 1
            care = request.form.get('care')

            contractor = Contractor(id=id, name=name, title=title, representative=representative, zip=zip,
             prefecture=prefecture, city=city, town=town, address=address, bldg=bldg, tel=tel, registered_by=registered_by)

            db.session.add(contractor)
            
            if care:
                care = Satiscare(contractor_id=id, membership=care)
                db.session.add(care)

            db.session.commit()

            flash('パートナーを登録しました。', 'success')

            return redirect(url_for('contractor.index'))

    return render_template('contractor/register.html', form=form)

# show and update customer profile
@contractor.route('/contractor/<int:id>')
@contractor.route('/contractor/<int:id>/<mode>')
def profile(id, mode=None):
    contractor = Contractor.query.get(id)

    if mode == 'edit':
        return '編集'

    return render_template('contractor/profile.html', contractor=contractor)
