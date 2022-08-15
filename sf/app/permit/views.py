from crypt import methods
from wsgiref import headers
import requests, json

from flask import Blueprint, render_template, current_app, jsonify, request, flash, redirect, url_for

from ..utils import get_contractor

from .forms import PermitRegisterForm

permit = Blueprint('permit', __name__, url_prefix='/permit')


@permit.route('/api')
def api():
    endpoint = 'https://opendata.resas-portal.go.jp/api/v1/prefectures'

    header = {
        "X-API-KEY":current_app.config['X_API_KEY']
    }

    req = requests.get(endpoint, headers=header).json()
    # content = json.loads(res.content)
    return req
    # return render_template('test.html', req=req.json)


@permit.route('/register/<int:contractor_id>', methods=['GET', 'POST'])
def register(contractor_id):

    contractor = get_contractor(contractor_id)
    form = PermitRegisterForm()

    if form.validate_on_submit():

        flash('許可情報を登録しました。', 'success')
        
        return redirect(url_for('contractor.profile', id=contractor_id))

    return render_template('permit/register.html', contractor=contractor, form=form)


@permit.route('/city/<prefecture>')
def city(prefecture):

    endpoint = 'https://opendata.resas-portal.go.jp/api/v1/cities'

    header = {
        # "Content-Type":"application/json",
        "X-API-KEY":current_app.config['X_API_KEY']
    }

    params = {
        "prefCode" : prefecture
    }


    res = requests.get(endpoint, headers=header, params=params)
    content = json.loads(res.content)
    # return f'{content["result"]}'

    cityArray = []

    for c in content['result']:
        cityObj = {}
        cityObj['code'] = c['cityCode']
        cityObj['name'] = c['cityName']
        cityArray.append(cityObj)

    return jsonify({'cities' : cityArray})


@permit.route('/<int:contractor_id>/<int:id>')
@permit.route('/<int:contractor_id>/<int:id>/<mode>', methods=['GET', 'POST'])
def details(contractor_id, id, mode=None):
    
    contractor = get_contractor(contractor_id)

    if mode == 'edit':
        return '編集'

    return render_template('permit/details.html', contractor=contractor)