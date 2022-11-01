from wsgiref import validate
from flask_wtf import FlaskForm
from wtforms import IntegerField, FileField, SelectField, DateField, BooleanField, StringField, SelectMultipleField
from wtforms.validators import NumberRange, DataRequired, InputRequired
from flask_wtf.file import FileAllowed

from ..models import Item


class ContractRegisterForm(FlaskForm):
    shop_id = SelectField('対象事業所', validators=[InputRequired('対象の事業所を選択してください。')])
    contractor_id = IntegerField('パートナーID', validators=[DataRequired('入力必須。'),
        NumberRange(min=1, max=99999, message='無効なIDです。')])
    contractor_name = StringField('PT名', validators=[DataRequired('PT名は必須です。')])
    item_id = SelectField('契約種類', validators=[DataRequired('契約種類は必須です。')])
    effective_from = DateField('契約有効開始日', validators=[DataRequired('契約の有効開始日を入力して下さい。')])
    expires_on = DateField('契約終了日', validators=[DataRequired('契約の終了日を入力して下さい。')])
    auto_extention = BooleanField('自動更新')
    # contract_copy = FileField('契約書コピー', validators=[FileAllowed(['pdf', 'PDF'], '登録可能なファイルはPDFのみです。')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_item_id()

    def _set_item_id(self):
        items = Item.query.all()
        # set item_id from db as tuple(value, text)
        self.item_id.choices = [('', '')]+[(item.id, item.name) for item in items]


class ContractEditForm(FlaskForm):
    item_id = SelectField('契約種類', validators=[DataRequired('契約種類は必須です。')])
    effective_from = DateField('契約有効開始日', validators=[DataRequired('契約の有効開始日を入力して下さい。')])
    expires_on = DateField('契約終了日', validators=[DataRequired('契約の終了日を入力して下さい。')])
    auto_extention = BooleanField('自動更新')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_item_id()

    def _set_item_id(self):
        items = Item.query.all()
        # set item_id from db as tuple(value, text)
        self.item_id.choices = [('', '')]+[(item.id, item.name) for item in items]

class AddShopForm(FlaskForm):
    shop_id = SelectField('契約事業所', validators=[InputRequired('契約事業所は必須です。')])
