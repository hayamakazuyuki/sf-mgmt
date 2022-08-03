import os, io

from flask import Blueprint, render_template, request, current_app, send_file, abort
from google.cloud import storage

from .models import Contract, Shop

contract = Blueprint('contract', __name__)

@contract.route('/contract/<int:id>')
def contract_details(id):

    contract = Contract.query.get(id)
    shop = Shop.query.get((contract.customer_id, contract.shop_id))

    return render_template('contract/contract-details.html', contract=contract, shop=shop)
    

@contract.route('/contract/get_copy/<int:id>')
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