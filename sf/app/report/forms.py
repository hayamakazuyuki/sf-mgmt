from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, DateField
from wtforms.validators import DataRequired

from ..models import Item

class VolumeReportForm(FlaskForm):
    month = DateField('対象月', validators=[DataRequired('対象の月を入力して下さい。')])
    item_id = SelectField('種別', coerce=int)
    name = StringField('品名', validators=[DataRequired('入力は必須です。')])
    volume = IntegerField('重量(kg)', validators=[DataRequired('kgで重量を入力して下さい。')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_item_id()

    def _set_item_id(self):
        items = Item.query.all()
        # set item_id from db as tuple(value, text)
        self.item_id.choices = [(item.id, item.abbrev) for item in items]
