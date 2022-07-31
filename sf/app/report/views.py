from flask import Blueprint, render_template, request, redirect, url_for, flash

from ..extentions import db

from ..models import VolumeReport

from .forms import VolumeReportForm

report = Blueprint('report', __name__)


@report.route('/report')
def index():
    return 'report'


@report.route('/report/register/<int:customer_id>/<int:shop_id>/<int:contractor_id>', methods=['GET', 'POST'])
def register(customer_id, shop_id, contractor_id):
    form = VolumeReportForm()

    if form.validate_on_submit():
        month = request.form['month']
        item_id = request.form['item_id']
        name = request.form['name']
        volume = request.form['volume']
        registered_by = 'hayama@sfinter.com'

        volume = VolumeReport(customer_id=customer_id, shop_id=shop_id, contractor_id=contractor_id, month=month,
            item_id=item_id, name=name, volume=volume, registered_by=registered_by)

        db.session.add(volume)
        db.session.commit()

        flash('登録しました', 'success')

        return redirect(url_for('customer.index'))

    return render_template('report/register.html', form=form)
