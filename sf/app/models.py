from .extentions import db
from sqlalchemy import func

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

class Satiscare(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contractor_id = db.Column(db.Integer, db.ForeignKey('contractor.id'), unique=True, nullable=False)
    membership = db.Column(db.Integer, nullable=True)


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
