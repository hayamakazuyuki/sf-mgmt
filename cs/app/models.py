from .extentions import db
from sqlalchemy import ForeignKeyConstraint, func


# class Parent(db.Model):
#     id = db.Column(db.Integer, primary_key=True, auto_increment=True)
#     name = db.Column(db.String(100), nullable=False)
#     registered_by = db.Column(db.Integer, nullable=False)
#     registered_at = db.Column(db.DateTime, default=func.now())
#     customers = db.relationship('Customer', backref = db.backref('parent', lazy=True))


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
    # collection_requests = db.relationship('CollectionRequest', backref=db.backref('shop', lazy=True))


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
    permits = db.relationship('Permit', backref=db.backref('contractor', lazy=True))


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
    licensed_items = db.relationship('LicensedItem', backref=db.backref('license', lazy=True))


class LicensedItem(db.Model):
    license_id = db.Column(db.Integer, db.ForeignKey('license.id'), primary_key=True)
    ind_waste_id = db.Column(db.Integer, db.ForeignKey('ind_waste.id'), primary_key=True)


class IndWaste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    licensed_items = db.relationship('LicensedItem', backref=db.backref('ind_waste', lazy=True))


class Permit(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    contractor_id = db.Column(db.Integer, db.ForeignKey('contractor.id'), nullable=False)
    prefecture = db.Column(db.Integer, db.ForeignKey('issuer.id'), nullable=False)
    city = db.Column(db.String, nullable=False)
    permit_type_id = db.Column(db.Integer, db.ForeignKey('permit_type.id'), nullable=False)
    effective_from = db.Column(db.Date, nullable=False)
    expires_on = db.Column(db.Date, nullable=False)
    copy_url = db.Column(db.String(2083))

class PermitType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    permits = db.relationship('Permit', backref=db.backref('permit_type', lazy=True))


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    customer_id = db.Column(db.Integer, nullable=False)
    contractor_id = db.Column(db.Integer, db.ForeignKey('contractor.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    effective_from = db.Column(db.Date, nullable=False)
    expires_on = db.Column(db.Date, nullable=False)
    auto_extention = db.Column(db.Boolean, nullable=True)
    file_name = db.Column(db.String(255), nullable=True)
    shops = db.relationship('ContractShop', backref=db.backref('contract', lazy=True))


class ContractShop(db.Model):
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.id'), primary_key=True)
    customer_id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, primary_key=True)

    __table_args__ = (ForeignKeyConstraint(['customer_id', 'shop_id'], ['shop.customer_id', 'shop.id']),)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    abbrev = db.Column(db.String(10))
    contracts = db.relationship('Contract', backref=db.backref('item', lazy=True))
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

class CollectionRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    customer_id = db.Column(db.Integer, nullable=False)
    shop_id = db.Column(db.Integer, nullable=False)
    details = db.Column(db.String, nullable=False)
    preferreddate = db.Column(db.Date, nullable=True)
    fluorescentlamp = db.Column(db.Integer, nullable=True)
    battery = db.Column(db.Integer, nullable=True)
    consumerelectronics = db.Column(db.Integer, nullable=True)
    registered_by = db.Column(db.String, nullable=False)
    registered_at = db.Column(db.DateTime, default=func.now())

    # __table_args__ = (ForeignKeyConstraint(['customer_id', 'shop_id'], ['shop.customer_id', 'shop.id']))

class Issuer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    licenses = db.relationship('License', backref=db.backref('issuer', lazy=True))
    permits = db.relationship('Permit', backref=db.backref('issuer', lazy=True))

class LicenseType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    licenses = db.relationship('License', backref=db.backref('license_type', lazy=True))