from unicodedata import name
from flask_wtf import FlaskForm
from wtforms import IntegerField, FileField, SelectField
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
    contract_copy = FileField('契約書コピー', validators=[FileAllowed('pdf', '登録可能なファイルはPDFのみです。')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_item_id()

    def _set_item_id(self):
        items = Item.query.all()
        # set item_id from db as tuple(value, text)
        self.item_id.choices = [(item.id, item.name) for item in items]
