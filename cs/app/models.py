from .extentions import db
from sqlalchemy import func

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
    registered_at = db.Column(db.DateTime, default=func.now())


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
    registered_at = db.Column(db.DateTime, default=func.now())


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    abbrev = db.Column(db.String(10))
    volume_reports = db.relationship('VolumeReport', backref=db.backref('item', lazy=True))


class VolumeReport(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    customer_id = db.Column(db.Integer, nullable=False)
    shop_id = db.Column(db.Integer, nullable=False)
    contractor_id = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Date, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False) 
    name = db.Column(db.String(50), nullable=False)
    volume = db.Column(db.Integer, nullable=False)
