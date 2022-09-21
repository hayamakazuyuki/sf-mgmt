import io

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, abort, send_file, make_response
from google.cloud import storage

from ..extentions import db

from ..models import Contract, Customer, Contractor, Shop
from .forms import ContractRegisterForm


contract = Blueprint('contract', __name__, url_prefix='/contract')


@contract.route('/')
def index():
    return render_template('contract/index.html')


@contract.route('/register/<int:customer_id>', methods=['GET', 'POST'])
def register(customer_id):

    customer = Customer.query.get(customer_id)

    form = ContractRegisterForm()

    if form.validate_on_submit():
        customer_id = request.form['customer_id']
        contractor_id = request.form['contractor_id']
        item_id = request.form['item_id']
        effective_from = request.form['effective_from']
        expires_on = request.form['expires_on']
        auto_extention = request.form.get('auto_extention')
        if auto_extention:
            auto_extention = 1
        registered_by = 1

        contract = Contract(customer_id=customer_id, contractor_id=contractor_id,
            item_id=item_id, effective_from=effective_from, expires_on=expires_on, auto_extention=auto_extention, 
            registered_by=registered_by)

        db.session.add(contract)
        db.session.commit()

        # get the contract id
        contract_id = str(contract.id)

        file = request.files.get('contract_copy')

        if file:
            try:
                bucket_name = current_app.config['GCS_BUCKET_NAME']
                file_name = customer_id.zfill(5) + contractor_id.zfill(5) + contract_id + '.pdf'

                storage_client = storage.Client()

                bucket = storage_client.bucket(bucket_name)

                blob = bucket.blob('contract/' + file_name)
                blob.upload_from_string(file.read(), content_type=file.content_type)

                contract = Contract.query.get(contract.id)
                contract.file_name = file_name
                db.session.commit()

            except Exception:
                pass

        flash('契約を登録しました。', 'success')

        return redirect(url_for('customer.profile', id=customer_id))

    return render_template('contract/register.html', customer=customer, form=form)


@contract.route('/search_contractor')
def search_contractor():
    q = request.args.get('q')

    if q:
        search = "%{}%".format(q)
        contractors = Contractor.query.filter(Contractor.name.like(search)).all()
        count = len(contractors)

        change_keyword = None

        if count > 21:
            change_keyword = '検索結果が20件を超えています。検索ワードを変えて下さい。'
            contractors = None
        
        else:
            pass

        return render_template('contract/search_contractor.html', contractors=contractors, change_keyword=change_keyword)

    return render_template('contract/search_contractor.html')


@contract.route('/contractor/<int:id>')
def get_contractor(id):

    contractor = Contractor.query.get(id)

    if contractor:
        return {'name': contractor.name}

    else:
        return {'name': ''}


@contract.route('/<int:id>')
def detail(id):
    contract = Contract.query.get_or_404(id)

    return render_template('contract/details.html', contract=contract)


@contract.route('/copy/<int:id>')
def contract_copy(id):

    contract = Contract.query.get(id)

    try:
        customer_id = str(contract.customer_id)
        contractor_id = str(contract.contractor_id)
        contract_id = str(contract.id)

        bucket_name = current_app.config['GCS_BUCKET_NAME']

        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob('contract/' + customer_id.zfill(5) + contractor_id.zfill(5) + contract_id + '.pdf')
        pdf_binary = blob.download_as_bytes()

        return send_file(
            io.BytesIO(pdf_binary),
            mimetype='application/pdf',
            as_attachment=False,
            attachment_filename='test.pdf'
        )

    except FileNotFoundError:
        abort(404)