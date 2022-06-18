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


class License(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    contractor_id = db.Column(db.Integer, nullable=False)
    issuer = db.Column(db.Integer, nullable=False)
    license_type = db.Column(db.Integer, nullable=False)
    reserved_num = db.Column(db.Integer, nullable=False)
    unique_num = db.Column(db.Integer, nullable=False)
    effective_from = db.Column(db.Date, nullable=False)
    expires_on = db.Column(db.Date, nullable=False)
    copy_url = db.Column(db.String(2083))


class Satiscare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contractor_id = db.Column(db.Integer, db.ForeignKey('contractor.id'), unique=True, nullable=False)
    membership = db.Column(db.Integer, nullable=True)


class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(100), nullable=False)
    registered_by = db.Column(db.Integer, nullable=False)
    registered_at = db.Column(db.DateTime, default=func.now())


class Customer(db.Model):
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
    registered_by = db.Column(db.Integer, nullable=False)
    registered_at = db.Column(db.DateTime, default=func.now())


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    contracts = db.relationship('Contract', backref=db.backref('item', lazy=True))


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    customer_id = db.Column(db.Integer, nullable=False)
    shop_id = db.Column(db.Integer, nullable=False)
    contractor_id = db.Column(db.Integer, db.ForeignKey('contractor.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    registered_by = db.Column(db.Integer, nullable=False)
    registered_at = db.Column(db.DateTime, default=func.now())


class Issuer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)

class LicenseType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class ParentAdminView(ModelView):
    form_excluded_columns = ['registered_at']

class ItemAdminView(ModelView):
    form_columns = ['id', 'name']
    column_list = ['id', 'name']

class IssuerAdminView(ModelView):
    form_columns = ['id', 'name']
    column_list = ['id', 'name']

class LicenseTypeAdminView(ModelView):
    form_columns = ['id', 'name']
    column_list = ['id', 'name']


admin.add_view(ParentAdminView(Parent, db.session))
admin.add_view(ItemAdminView(Item, db.session))
admin.add_view(IssuerAdminView(Issuer, db.session))
admin.add_view(LicenseTypeAdminView(LicenseType, db.session))
