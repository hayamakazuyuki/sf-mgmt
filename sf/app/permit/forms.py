from flask_wtf import FlaskForm

from wtforms import DateField, StringField, SelectField, FileField
from wtforms.validators import DataRequired, Optional, URL

class PermitRegisterForm(FlaskForm):
    prefecture = SelectField('都道府県', validators=[DataRequired('都道府県を選択して下さい。')])
    city = SelectField('市区町村', validators=[DataRequired('市区町村を選択して下さい。')])
    type = SelectField('種類', choices=[('', ''), ('1', '収集運搬'), ('2', '処分')], validators=[DataRequired('種類を選択して下さい。')])
    effective_from = DateField('許可の年月日', validators=[DataRequired('許可の年月日を入力してください。')])
    expires_on = DateField('許可の有効年月日', validators=[DataRequired('許可の有効年月日を入力してください。')])
    copy_url = StringField('許可証のリンクURL', validators=[Optional(), URL(require_tld=True, message='有効なURLを入力してください。')])
    license_copy = FileField('PDFアップロード')
