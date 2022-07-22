import os, io

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort, send_file
from google.cloud import storage

from ..extentions import db

from ..models import Contract, Shop
from .forms import ContractRegisterForm


contract = Blueprint('contract', __name__, url_prefix='/contract')


@contract.route('/')
def index():
    return render_template('contract/index.html')


@contract.route('/register/<int:customer_id>/<int:id>', methods=['GET', 'POST'])
def register(customer_id, id):

    shop = Shop.query.get_or_404((customer_id, id))
    form = ContractRegisterForm()

    if form.validate_on_submit():
        customer_id = request.form['customer_id']
        shop_id = request.form['shop_id']
        contractor_id = request.form['contractor_id']
        item_id = request.form['item_id']
        effective_from = request.form['effective_from']
        expires_on = request.form['expires_on']
        auto_extention = request.form.get('auto_extention')
        if auto_extention:
            auto_extention = 1
        registered_by = 1

        contract = Contract(customer_id=customer_id, shop_id=shop_id, contractor_id=contractor_id,
            item_id=item_id, effective_from=effective_from, expires_on=expires_on, auto_extention=auto_extention, 
            registered_by=registered_by)

        db.session.add(contract)
        db.session.commit()

        # retrieve the contract id
        contract_id = str(contract.id)

        file = request.files.get('contract_copy')

        if file:
            try:
                bucket_name = current_app.config['GCS_BUCKET_NAME']

                storage_client = storage.Client()

                bucket = storage_client.bucket(bucket_name)

                blob = bucket.blob('contract/' + customer_id + '/' + shop_id + '/' + contractor_id + '/' + contract_id + '.pdf')
                blob.upload_from_string(file.read(), content_type=file.content_type)

                contract = Contract.query.get(contract.id)
                contract.has_copy = 1
                db.session.commit()

            except Exception:
                pass

        flash('契約を登録しました。', 'success')

        return redirect(url_for('customer.shop_profile', customer_id=customer_id, id=shop_id))

    return render_template('contract/register.html', shop=shop, form=form)


@contract.route('/<int:id>')
def detail(id):
    contract = Contract.query.get_or_404(id)
    shop = Shop.query.get_or_404((contract.customer_id, contract.shop_id))

    return render_template('contract/details.html', contract=contract, shop=shop)


@contract.route('/get_copy/<int:id>')
def get_copy(id):

    contract = Contract.query.get(id)

    try:
        customer_id = str(contract.customer_id)
        shop_id = str(contract.shop_id)
        contractor_id = str(contract.contractor_id)
        contract_id = str(contract.id)

        bucket_name = current_app.config['GCS_BUCKET_NAME']

        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob('contract/' + customer_id + '/' + shop_id + '/' + contractor_id + '/' + contract_id + '.pdf')
        pdf_binary = blob.download_as_bytes()

        return send_file(
            io.BytesIO(pdf_binary),
            mimetype='application/pdf',
            as_attachment=False,
            attachment_filename='test.pdf'
        )

    except FileNotFoundError:
        abort(404)