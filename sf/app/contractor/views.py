from flask import Blueprint, render_template, request, flash, redirect, url_for

from ..extentions import db

from ..models import Contractor, Satiscare, License

from .forms import ContractorForm, LicenseRegisterForm

contractor = Blueprint('contractor', __name__, url_prefix='/contractor')

@contractor.route('/')
def index():

    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)

    if q:
        search = "%{}%".format(q)
        contractors = Contractor.query.filter(Contractor.name.like(search)).paginate(page=page, per_page=20)
        count = len(Contractor.query.filter(Contractor.name.like(search)).all())

        return render_template('contractor/index.html', page=page, contractors=contractors, count=count, search=search)

    else:
        contractors = Contractor.query.paginate(page=page, per_page=20)
        count = len(Contractor.query.all())

        return render_template('contractor/index.html', contractors=contractors, page=page, count=count)


@contractor.route('/register', methods=['GET', 'POST'])
def register():

    form = ContractorForm()

    if form.validate_on_submit():

        id = request.form['id']

        # check if id already exists in the db
        exists = Contractor.query.get(id)

        if exists:
            return redirect(url_for('contractor.profile', id=id))

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
            care = request.form.get('care')

            contractor = Contractor(id=id, name=name, title=title, representative=representative, zip=zip,
             prefecture=prefecture, city=city, town=town, address=address, bldg=bldg, registered_by=registered_by)

            db.session.add(contractor)

            if care:
                care = Satiscare(contractor_id=id, membership=care)
                db.session.add(care)

            db.session.commit()

            flash('パートナーを登録しました。', 'success')

            return redirect(url_for('contractor.profile', id=id))

    return render_template('contractor/register.html', form=form)


# show and update contractor profile
@contractor.route('/<int:id>')
@contractor.route('/<int:id>/<mode>', methods=['GET', 'POST'])
def profile(id, mode=None):
    contractor = Contractor.query.get(id)
    licenses = License.query.filter(License.contractor_id == id).all()

    if mode == 'edit':
        form = ContractorForm()

        if form.validate_on_submit():

            contractor.name = request.form['name']
            contractor.title = request.form.get('title')
            contractor.representative = request.form['representative']
            contractor.zip = request.form['zip']
            contractor.prefecture = request.form['prefecture']
            contractor.city = request.form['city']
            contractor.town = request.form['town']
            contractor.address = request.form.get('address')
            contractor.bldg = request.form.get('bldg')
            contractor.registered_by = 1

            # if care checkbox is checked
            care = request.form.get('care')

            # if already a satiscare member 
            is_member = Satiscare.query.filter_by(contractor_id=id).first()

            if is_member and not care:
                member = Satiscare.query.filter_by(contractor_id=id).first()
                db.session.delete(member)

            elif not is_member and care:
                care = Satiscare(contractor_id=id, membership=care)
                db.session.add(care)

            else:
                pass

            db.session.commit()

            flash('パートナー情報を更新しました。', 'success')

            return redirect(url_for('contractor.profile', id=id))

        return render_template('contractor/edit.html', contractor=contractor, form=form)

    return render_template('contractor/profile.html', contractor=contractor, licenses=licenses)


#register license
@contractor.route('/<int:id>/license/register', methods=['GET', 'POST'])
def license_register(id):
    contractor = Contractor.query.get(id)

    form = LicenseRegisterForm()

    if form.validate_on_submit():
        contractor_id = id
        issuer_id = request.form['issuer']
        license_type_id = request.form['license_type']
        reserved_num = request.form['reserved_num']
        unique_num = request.form['unique_num']
        effective_from = request.form['effective_from']
        expires_on = request.form['expires_on']
        copy_url = request.form.get('copy_url')
        registered_by = 1

        license = License(contractor_id=contractor_id, issuer_id=issuer_id, license_type_id=license_type_id, reserved_num=reserved_num,
            unique_num=unique_num, effective_from=effective_from, expires_on=expires_on, copy_url=copy_url, registered_by=registered_by)

        db.session.add(license)
        db.session.commit()

        flash('許可証情報を登録しました。', 'success')

        return redirect(url_for('contractor.profile', id=id))
        # return request.form
    return render_template('contractor/license-register.html', contractor=contractor, form=form)


# license detail
@contractor.route('/<int:contractor_id>/license/<int:id>')
@contractor.route('/<int:contractor_id>/license/<int:id>/<mode>', methods=['GET', 'POST'])
def license_detail(contractor_id, id, mode=None):
    contractor = Contractor.query.get(contractor_id)
    license = License.query.get(id)

    if mode == 'edit':
        issuer_id = license.issuer_id
        license_type_id = license.license_type_id
        reserved_num = license.reserved_num

        form = LicenseRegisterForm(issuer=issuer_id, license_type=license_type_id, reserved_num=reserved_num)

        if form.validate_on_submit():
            license.issuer_id = request.form['issuer']
            license.license_type_id = request.form['license_type']
            license.reserved_num = request.form['reserved_num']
            license.unique_num = request.form['unique_num']
            license.effective_from = request.form['effective_from']
            license.expires_on = request.form['expires_on']
            license.copy_url = request.form.get('copy_url')
            license.registered_by = 1

            db.session.commit()

            flash('許可証情報を更新しました。', 'success')

            return render_template('contractor/license-detail.html', contractor=contractor, license=license)

        return render_template('contractor/license-edit.html', contractor=contractor, license=license, form=form)

    return render_template('contractor/license-detail.html', contractor=contractor, license=license)


