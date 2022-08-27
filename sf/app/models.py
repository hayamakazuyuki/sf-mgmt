from .extentions import db, admin
from sqlalchemy import func
from flask_admin.contrib.sqla import ModelView


class Contractor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(50), nullable=True)
    representative = db.Column(db.String(50), nullable=False)
    zip = db.Column(db.String(7), nullable=False)
    prefecture = db.Column(db.String(4), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    town = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100))
    bldg = db.Column(db.String(50))
    registered_by = db.Column(db.Integer, nullable=False)
    registered_at = db.Column(db.DateTime, default=func.now())
    satiscare = db.relationship('Satiscare', backref='contractor', uselist=False)
    contracts = db.relationship('Contract', backref=db.backref('contractor', lazy=True))
    licenses = db.relationship('License', backref=db.backref('contractor', lazy=True))


class License(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    contractor_id = db.Column(db.Integer, db.ForeignKey('contractor.id'), nullable=False)
    issuer_id = db.Column(db.Integer, db.ForeignKey('issuer.id'), nullable=False)
    license_type_id = db.Column(db.Integer, db.ForeignKey('license_type.id'), nullable=False)
    reserved_num = db.Column(db.Integer, nullable=False)
    unique_num = db.Column(db.String(6), nullable=False)
    effective_from = db.Column(db.Date, nullable=False)
    expires_on = db.Column(db.Date, nullable=False)
    copy_url = db.Column(db.String(2083))
    registered_by = db.Column(db.Integer, nullable=False)
    registered_at = db.Column(db.DateTime, default=func.now())


class Permit(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    contractor_id = db.Column(db.Integer, db.ForeignKey('contractor.id'), nullable=False)
    prefecture = db.Column(db.Integer, db.ForeignKey('issuer.id'), nullable=False)
    city = db.Column(db.String, nullable=False)
    permit_type_id = db.Column(db.Integer, db.ForeignKey('permit_type.id'), nullable=False)
    effective_from = db.Column(db.Date, nullable=False)
    expires_on = db.Column(db.Date, nullable=False)
    copy_url = db.Column(db.String(2083))
    registered_by = db.Column(db.String(255), nullable=False)
    registered_at = db.Column(db.DateTime, default=func.now())


class Satiscare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contractor_id = db.Column(db.Integer, db.ForeignKey('contractor.id'), unique=True, nullable=False)
    membership = db.Column(db.Integer, nullable=True)

# for refactoring
class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(100), nullable=False)
    registered_by = db.Column(db.Integer, nullable=False)
    registered_at = db.Column(db.DateTime, default=func.now())
    customers = db.relationship('Customer', backref = db.backref('parent', lazy=True))


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(50), nullable=True)
    representative = db.Column(db.String(50), nullable=False)
    zip = db.Column(db.String(7), nullable=False)
    prefecture = db.Column(db.String(4), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    town = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100))
    bldg = db.Column(db.String(50))
    registered_by = db.Column(db.String(255), nullable=False)
    registered_at = db.Column(db.DateTime, default=func.now())
    shops = db.relationship('Shop', backref=db.backref('customer', lazy=True))


class Shop(db.Model):
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    shop_number = db.Column(db.String(15), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    zip = db.Column(db.String(7), nullable=False)
    prefecture = db.Column(db.String(4), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    town = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100))
    bldg = db.Column(db.String(50))
    registered_by = db.Column(db.String(255), nullable=False)
    registered_at = db.Column(db.DateTime, default=func.now())


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    abbrev = db.Column(db.String(10))
    contracts = db.relationship('Contract', backref=db.backref('item', lazy=True))


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    customer_id = db.Column(db.Integer, nullable=False)
    shop_id = db.Column(db.Integer, nullable=False)
    contractor_id = db.Column(db.Integer, db.ForeignKey('contractor.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    effective_from = db.Column(db.Date, nullable=False)
    expires_on = db.Column(db.Date, nullable=False)
    auto_extention = db.Column(db.Boolean, nullable=True)
    has_copy = db.Column(db.Boolean, nullable=True)
    registered_by = db.Column(db.Integer, nullable=False)
    registered_at = db.Column(db.DateTime, default=func.now())


class Issuer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    licenses = db.relationship('License', backref=db.backref('issuer', lazy=True))
    permits = db.relationship('Permit', backref=db.backref('issuer', lazy=True))


class LicenseType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    licenses = db.relationship('License', backref=db.backref('license_type', lazy=True))


class PermitType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    permits = db.relationship('Permit', backref=db.backref('permit_type', lazy=True))


class VolumeReport(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    customer_id = db.Column(db.Integer, nullable=False)
    shop_id = db.Column(db.Integer, nullable=False)
    contractor_id = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Date, nullable=False)
    item_id = db.Column(db.Integer, nullable=False) 
    name = db.Column(db.String(50), nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    registered_by = db.Column(db.Integer, nullable=False)
    registered_at = db.Column(db.DateTime, default=func.now())


class ParentAdminView(ModelView):
    form_excluded_columns = ['registered_at']

class ItemAdminView(ModelView):
    form_columns = ['id', 'name', 'abbrev']
    column_list = ['id', 'name', 'abbrev']

class IssuerAdminView(ModelView):
    form_columns = ['id', 'name']
    column_list = ['id', 'name']

class LicenseTypeAdminView(ModelView):
    form_columns = ['id', 'name']
    column_list = ['id', 'name']

class PermitTypeAdminView(ModelView):
    form_columns = ['name']
    # column_list = ['id', 'name']


admin.add_view(ParentAdminView(Parent, db.session))
admin.add_view(ItemAdminView(Item, db.session))
admin.add_view(IssuerAdminView(Issuer, db.session))
admin.add_view(LicenseTypeAdminView(LicenseType, db.session))
admin.add_view(ModelView(Customer, db.session, endpoint='customerview'))
admin.add_view(PermitTypeAdminView(PermitType, db.session))
