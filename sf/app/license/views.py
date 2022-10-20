from crypt import methods
import io
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, abort, send_file
from ..extentions import db, storage
from ..models import License, LicensedItem

from .forms import LicenseRegisterForm, LicensedIndWasteForm

from ..utils import get_contractor, get_license

license = Blueprint('license', __name__, url_prefix='/license')


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

            db.session.commit()
            flash('許可証情報を登録しました。', 'success')

            return redirect(url_for('contractor.profile', id=contractor_id))

        # if pdf attachement.
        else:
            bucket_name = current_app.config['GCS_BUCKET_NAME']

            storage_client = storage.Client()

            bucket = storage_client.bucket(bucket_name)

            blob = bucket.blob('license/' + issuer_id.zfill(3) + license_type_id + reserved_num + unique_num + '.pdf')
            blob.upload_from_string(file.read(), content_type=file.content_type)

            db.session.commit()

            flash('許可証情報を登録しました。', 'success')

            return redirect(url_for('contractor.profile', id=contractor_id))

    return render_template('license/register.html', form=form, contractor=contractor)


# industrial waste license details
@license.route('/details/<int:id>')
@license.route('/details/<int:id>/<mode>', methods=['GET', 'POST'])
def details(id, mode=None):

    license = get_license(id)

    # get only licensed industrial waste ids
    result = LicensedItem.query.filter_by(license_id=id).with_entities(LicensedItem.ind_waste_id).all()
    licensed_items = [ e[0] for e in result ]

    if mode == 'edit':

        form = LicenseRegisterForm(issuer=license.issuer_id, license_type=license.license_type_id,
                                    reserved_num=license.reserved_num)
        
        select = ''
        if license.copy_url:
            select = 'url'
        else:
            select = 'pdf'

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

            return redirect(url_for('license.details', contractor_id=license.contractor_id, id=id))

        return render_template('license/edit.html', license=license, form=form, select=select)

    return render_template('license/details.html', license=license, licensed_items=licensed_items)


@license.route('/items/<int:id>', methods=['GET', 'POST'])
def license_items(id):
    license = get_license(id)

    form = LicensedIndWasteForm()

    if form.validate_on_submit():

        reqs = request.form.getlist('item')

        if reqs:
            for req in reqs:
                licenseditem = LicensedItem(license_id=id, ind_waste_id=req)
                db.session.add(licenseditem)

        try:
            db.session.commit()
            flash('許可証情報を更新しました。', 'success')

        except:
            flash('内容をご確認ください。', 'info')

        return redirect(url_for('license.details', id=id))

    return render_template('license/edit-details.html', license=license, form=form)


@license.route('/<filename>')
def get_license_copy(filename):

    try:
        bucket_name = current_app.config['GCS_BUCKET_NAME']
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob('license/' + filename  + '.pdf')
        pdf_binary = blob.download_as_bytes()

        return send_file(
            io.BytesIO(pdf_binary),
            mimetype='application/pdf',
            as_attachment=False,
            attachment_filename=filename + '.pdf'
        )

    except FileNotFoundError:
        abort(404)
