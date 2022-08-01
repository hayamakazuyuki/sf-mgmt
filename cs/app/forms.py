from flask_wtf import FlaskForm
from wtforms import TextAreaField, BooleanField, DateField
from wtforms.validators import DataRequired, Optional


class CollectionRequestForm(FlaskForm):
    details = TextAreaField('依頼内容', validators=[DataRequired('依頼内容を入力してください。')])
    preferreddate = DateField('収集希望日', validators=[Optional()])
    fluorescentlamp = BooleanField('蛍光灯')
    battery = BooleanField('乾電池')
    consumerelectronics = BooleanField('家電リサイクル品')
