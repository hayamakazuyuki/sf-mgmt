from flask_wtf import FlaskForm

from wtforms import DateField, StringField, SelectField, FileField
from wtforms.validators import DataRequired, Optional, URL

class PermitRegisterForm(FlaskForm):
    effective_from = DateField('許可の年月日', validators=[DataRequired('許可の年月日を入力してください。')])
    expires_on = DateField('許可の有効年月日', validators=[DataRequired('許可の有効年月日を入力してください。')])
    copy_url = StringField('許可証のリンクURL', validators=[Optional(), URL(require_tld=True, message='有効なURLを入力してください。')])
    license_copy = FileField('PDFアップロード')
