from wsgiref import validate
from flask_wtf import FlaskForm
from wtforms import IntegerField, FileField, SelectField, DateField, BooleanField, StringField, SelectMultipleField
from wtforms.validators import NumberRange, DataRequired
from flask_wtf.file import FileAllowed

from ..models import Item


class ContractRegisterForm(FlaskForm):
    customer_id = IntegerField('取引先ID', validators=[DataRequired('取引先IDは必須です。'),
        NumberRange(min=1, max=99999, message='有効なIDを入力してください。')])
    contractor_id = IntegerField('パートナーID', validators=[DataRequired('入力必須。'),
        NumberRange(min=1, max=99999, message='無効なIDです。')])
    contractor_name = StringField('PT名', validators=[DataRequired('PT名は必須です。')])
    item_id = SelectField('契約種類', validators=[DataRequired('契約種類は必須です。')])
    effective_from = DateField('契約有効開始日', validators=[DataRequired('契約の有効開始日を入力して下さい。')])
    expires_on = DateField('契約終了日', validators=[DataRequired('契約の終了日を入力して下さい。')])
    auto_extention = BooleanField('自動更新')
    contract_copy = FileField('契約書コピー', validators=[FileAllowed(['pdf', 'PDF'], '登録可能なファイルはPDFのみです。')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_item_id()

    def _set_item_id(self):
        items = Item.query.all()
        # set item_id from db as tuple(value, text)
        self.item_id.choices = [('', '')]+[(item.id, item.name) for item in items]
