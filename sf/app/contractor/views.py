from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app

from ..extentions import db, storage

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
        file = request.files.get('license_copy')

        registered_by = 1

        # check if the license already registered. if already registered, redirect to the license details.
        exists = License.query.filter_by(issuer_id=issuer_id).filter_by(license_type_id=license_type_id)\
            .filter_by(reserved_num=reserved_num).filter_by(unique_num=unique_num).first()

        if exists:
            flash('既に登録があります。', 'info')

            return redirect(url_for('contractor.license_detail', contractor_id=exists.contractor_id, id=exists.id))

        # register, if not already registered and copy_url
        license = License(contractor_id=contractor_id, issuer_id=issuer_id, license_type_id=license_type_id, reserved_num=reserved_num,
            unique_num=unique_num, effective_from=effective_from, expires_on=expires_on, copy_url=copy_url, registered_by=registered_by)

        db.session.add(license)

        if copy_url:

            db.session.commit()
            flash('許可証情報を登録しました。', 'success')

            return redirect(url_for('contractor.profile', id=id))

        # if pdf attachement.
        else:
            try:
                bucket_name = current_app.config['GCS_BUCKET_NAME']

                storage_client = storage.Client()

                bucket = storage_client.bucket(bucket_name)

                blob = bucket.blob('license/' + issuer_id.zfill(3) + license_type_id + reserved_num + unique_num + '.pdf')
                blob.upload_from_string(file.read(), content_type=file.content_type)

                db.session.commit()

                flash('許可証情報を登録しました。', 'success')

                return redirect(url_for('contractor.profile', id=id))

            except Exception:

                db.session.rollback()
                flash('許可証情報が登録出来ませんでした。', 'error')

                return redirect(url_for('contractor.profile', id=id))
                
    return render_template('contractor/license-register.html', contractor=contractor, form=form)
