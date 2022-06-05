from unicodedata import name
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import InputRequired, NumberRange
from wtforms_sqlalchemy.fields import QuerySelectField

from ..models import Item


def item_query():
    return Item.query


class ContractRegisterForm(FlaskForm):
    customer_id = IntegerField('取引先ID', validators=[InputRequired('取引先IDは必須です。'),
        NumberRange(min=1, max=99999, message='有効なIDを入力してください。')])
    shop_id = IntegerField('事業所ID', validators=[InputRequired('事業所IDは必須です。'),
        NumberRange(min=1, max=99999, message='有効なIDを入力してください。')])
    contractor_id = IntegerField('パートナーID', validators=[InputRequired('パートナーIDは必須です。'),
        NumberRange(min=1, max=99999, message='有効なIDを入力してください。')])
    item_id = QuerySelectField('契約', query_factory=item_query, allow_blank=True, get_label='name')
