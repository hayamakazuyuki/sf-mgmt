from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from ..extentions import db, storage
from ..models import License

from .forms import LicenseRegisterForm

from ..utils import get_contractor, get_license

license = Blueprint('license', __name__, url_prefix='/license')


@license.route('/')
def index():

    return 'ライセンス　ホーム'


#register industrial waste license
@license.route('/register/<int:contractor_id>', methods=['GET', 'POST'])
def register(contractor_id):

    contractor = get_contractor(contractor_id)

    form = LicenseRegisterForm()

    if form.validate_on_submit():
        contractor_id = contractor_id
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

            return redirect(url_for('license.details', contractor_id=exists.contractor_id, id=exists.id))

        # register, if not already registered and copy_url
        license = License(contractor_id=contractor_id, issuer_id=issuer_id, license_type_id=license_type_id, reserved_num=reserved_num,
            unique_num=unique_num, effective_from=effective_from, expires_on=expires_on, copy_url=copy_url, registered_by=registered_by)

        db.session.add(license)

        if copy_url:

            # db.session.commit()
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

    return render_template('license/register.html', form=form, contractor=contractor)


# industrial waste license details
@license.route('/<int:contractor_id>/<int:id>')
def details(contractor_id, id, mode=None):

    contractor = get_contractor(contractor_id)
    license = get_license(id)

    return render_template('license/details.html', contractor=contractor, license=license)

"""
@contractor.route('/<int:contractor_id>/license/<int:id>/<mode>', methods=['GET', 'POST'])

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
"""