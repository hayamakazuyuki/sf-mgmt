from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SelectField, FileField
from wtforms.validators import DataRequired, Regexp, Optional, URL

from ..models import Issuer, LicenseType


class IwLicenseRegisterForm(FlaskForm):
    issuer = SelectField('都道府県・政令市', validators=[DataRequired('必須です。')])
    license_type = SelectField('業の種類', validators=[DataRequired('選択してください。')])
    reserved_num = SelectField('都道府県・政令市用番号', choices=['',0,1,2,3,4,5,6,7,8,9], validators=[DataRequired('選択してください。')])
    unique_num = StringField('固有番号', validators=[Regexp('[0-9]{6}', message='数字のみ6桁です。'), DataRequired('入力してください。')])
    effective_from = DateField('許可の年月日', validators=[DataRequired('許可の年月日を入力してください。')])
    expires_on = DateField('許可の有効年月日', validators=[DataRequired('許可の有効年月日を入力してください。')])
    copy_url = StringField('許可証のリンクURL', validators=[Optional(), URL(require_tld=True, message='有効なURLを入力してください。')])
    license_copy = FileField('PDFアップロード')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_issuers()
        self._set_license_type()


    def _set_issuers(self):
        issuers = Issuer.query.all()
        # set issuers from db as tuple(value, text)
        self.issuer.choices = [('', '')]+[(issuer.id, '%03d' % issuer.id) for issuer in issuers]


    def _set_license_type(self):
        types = LicenseType.query.all()
        # set issuers from db as tuple(value, text)
        self.license_type.choices = [('')]+[(type.id) for type in types]
