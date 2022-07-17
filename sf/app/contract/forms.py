from unicodedata import name
from flask_wtf import FlaskForm
from wtforms import IntegerField, FileField, SelectField, DateField, BooleanField
from wtforms.validators import NumberRange, DataRequired
from flask_wtf.file import FileAllowed

from ..models import Item


class ContractRegisterForm(FlaskForm):
    customer_id = IntegerField('取引先ID', validators=[DataRequired('取引先IDは必須です。'),
        NumberRange(min=1, max=99999, message='有効なIDを入力してください。')])
    shop_id = IntegerField('事業所ID', validators=[DataRequired('事業所IDは必須です。'),
        NumberRange(min=1, max=99999, message='有効なIDを入力してください。')])
    contractor_id = IntegerField('パートナーID', validators=[DataRequired('パートナーIDは必須です。'),
        NumberRange(min=1, max=99999, message='有効なIDを入力してください。')])
    item_id = SelectField('契約種類', coerce=int)
    effective_from = DateField('契約有効開始日')
    expires_on = DateField('契約終了日')
    auto_extention = BooleanField('自動更新')
    contract_copy = FileField('契約書コピー', validators=[FileAllowed('pdf', '登録可能なファイルはPDFのみです。')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_item_id()

    def _set_item_id(self):
        items = Item.query.all()
        # set item_id from db as tuple(value, text)
        self.item_id.choices = [(item.id, item.name) for item in items]
