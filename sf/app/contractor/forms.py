from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, BooleanField, DateField, SelectField
from wtforms.validators import InputRequired, NumberRange, Length, URL

from ..models import Issuer, LicenseType

class ContractorForm(FlaskForm):
    id = IntegerField('PT ID', validators=[InputRequired('IDを入力して下さい。'),
        NumberRange(min=1, max=999999, message='有効なIDを入力して下さい。')])
    name = StringField('PT名', validators=[InputRequired('業者名は必須です。')])
    title = StringField('代表者役職名')
    representative = StringField('代表者名', validators=[InputRequired('代表者名は必須です。')])
    zip = StringField('郵便番号', validators=[InputRequired('郵便番号は必須です。'),
        Length(min=7, max=7, message='郵便番号は7桁です。')])
    prefecture = StringField('都道府県', validators=[InputRequired('都道府県は必須です。')])
    city = StringField('市区町村', validators=[InputRequired('市区町村は必須です。')])
    town = StringField('町域', validators=[InputRequired('町域は必須です。')])
    address = StringField('住所', validators=[InputRequired('住所は必須です。')])
    bldg = StringField('建物名等')
    care = BooleanField('サティスケア会員')


class LicenseRegisterForm(FlaskForm):
    issuer = SelectField('都道府県・政令市', validators=[InputRequired('必須です。')])
    license_type = SelectField('業の種類', choices=['',0,1,2,3,4,5,6,7,8,9], validators=[InputRequired('選択してください。')])
    reserved_num = SelectField('都道府県・政令市用番号', choices=['',0,1,2,3,4,5,6,7,8,9], validators=[InputRequired('選択してください。')])
    unique_num = IntegerField('固有番号', validators=[InputRequired('固有番号は必須です。'), NumberRange(max=999999, message='最大6桁です。')])
    effective_from = DateField('許可の年月日', validators=[InputRequired('許可の年月日を入力してください。')])
    expires_on = DateField('許可の有効年月日', validators=[InputRequired('許可の有効年月日を入力してください。')])
    copy_url = StringField('許可証のリンクURL', validators=[URL(require_tld=True, message='有効なURLを入力してください。')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_issuers()
        self._set_license_type()

    def _set_issuers(self):
        issuers = Issuer.query.all()
        # set issuers from db as tuple(value, text)
        self.issuer.choices = [('')]+[('%03d' % issuer.id) for issuer in issuers]

    def _set_license_type(self):
        types = LicenseType.query.all()
        # set issuers from db as tuple(value, text)
        self.license_type.choices = [('')]+[(type.id) for type in types]