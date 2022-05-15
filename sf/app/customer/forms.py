from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, BooleanField
from wtforms.validators import InputRequired, NumberRange, Length

class CustomerForm(FlaskForm):
    id = IntegerField('取引先ID', validators=[InputRequired('IDを入力して下さい。'),
        NumberRange(min=1, max=999999, message='有効なIDを入力して下さい。')])
    name = StringField('取引先名', validators=[InputRequired('取引先名は必須です。')])
    title = StringField('代表者役職名')
    representative = StringField('代表者名', validators=[InputRequired('代表者名は必須です。')])
    zip = StringField('郵便番号', validators=[InputRequired('郵便番号は必須です。'),
        Length(min=7, max=7, message='郵便番号は7桁です。')])
    prefecture = StringField('都道府県', validators=[InputRequired('都道府県は必須です。')])
    city = StringField('市区町村', validators=[InputRequired('市区町村は必須です。')])
    town = StringField('町域', validators=[InputRequired('町域は必須です。')])
    address = StringField('住所', validators=[InputRequired('住所は必須です。')])
    bldg = StringField('建物名等')
    is_inactive = BooleanField('休止')
