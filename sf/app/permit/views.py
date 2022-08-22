import requests

from flask import Blueprint, render_template, current_app, jsonify, request, flash, redirect, url_for
from ..extentions import db

from ..models import Permit

from ..utils import get_contractor, get_permit

from .forms import PermitRegisterForm

permit = Blueprint('permit', __name__, url_prefix='/permit')


@permit.route('/api')
def api():
    endpoint = 'https://opendata.resas-portal.go.jp/api/v1/prefectures'

    header = {
        "X-API-KEY":current_app.config['X_API_KEY']
    }

    r = requests.get(endpoint, headers=header).json()

    return r


@permit.route('/register/<int:contractor_id>', methods=['GET', 'POST'])
def register(contractor_id):

    contractor = get_contractor(contractor_id)
    form = PermitRegisterForm()

    if form.validate_on_submit():
        contractor_id = contractor_id
        prefecture = request.form['prefecture']
        city = request.form['city']
        permit_type_id = request.form['permit_type']
        effective_from = request.form['effective_from']
        expires_on = request.form['expires_on']
        copy_url = request.form.get('copy_url')
        file = request.files.get('permit_copy')
        registered_by = 'hayama@sfinter.com'

        # check if the permit already registered. if already registered, redirect to the permit details.
        exists = Permit.query.filter_by(contractor_id=contractor_id).filter_by(city=city)\
            .filter_by(permit_type_id=permit_type_id).first()

        if exists:
            flash('既に登録があります。', 'info')

            return redirect(url_for('permit.details', contractor_id=exists.contractor_id, id=exists.id))

        # register, if not already registered and copy_url
        permit = Permit(contractor_id=contractor_id, prefecture=prefecture, city=city, permit_type_id=permit_type_id,
            effective_from=effective_from, expires_on=expires_on, copy_url=copy_url, registered_by=registered_by)

        db.session.add(permit)

        if copy_url:

            db.session.commit()
            flash('許可証情報を登録しました。', 'success')

            return redirect(url_for('contractor.profile', id=contractor_id))



        # flash('許可情報を登録しました。', 'success')

        # return redirect(url_for('contractor.profile', id=contractor_id))

    return render_template('permit/register.html', contractor=contractor, form=form)


@permit.route('/city/<prefecture>')
def city(prefecture):

    endpoint = 'https://opendata.resas-portal.go.jp/api/v1/cities'

    header = {
        "X-API-KEY":current_app.config['X_API_KEY']
    }

    params = {
        "prefCode" : prefecture
    }

    r = requests.get(endpoint, headers=header, params=params).json()

    cityArray = []

    for c in r['result']:
        cityObj = {}
        cityObj['code'] = c['cityCode']
        cityObj['name'] = c['cityName']
        cityArray.append(cityObj)

    return jsonify({'cities' : cityArray})


@permit.route('/<int:contractor_id>/<int:id>')
@permit.route('/<int:contractor_id>/<int:id>/<mode>', methods=['GET', 'POST'])
def details(contractor_id, id, mode=None):
    
    contractor = get_contractor(contractor_id)
    permit = get_permit(id)

    if mode == 'edit':
        return '編集'

    return render_template('permit/details.html', contractor=contractor, permit=permit)
    