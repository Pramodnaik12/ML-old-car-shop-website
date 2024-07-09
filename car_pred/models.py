from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    is_admin = db.Column(db.Boolean, default=False)
    user_type = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean, default=False)  # New field for user type (buyer/seller)


   

class Buyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    user = db.relationship('User', backref=db.backref('buyer', uselist=False))
    # Add buyer-specific fields here

class Seller(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    user = db.relationship('User', backref=db.backref('seller', uselist=False))
    # Add seller-specific fields here

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_name = db.Column(db.String(150))
    company = db.Column(db.String(150))
    year_of_purchase = db.Column(db.Integer)
    price = db.Column(db.Float)
    kms_driven = db.Column(db.Float)
    fuel_type = db.Column(db.String(50))
    owner_name = db.Column(db.String(150))
    address = db.Column(db.String(250))
    contact_details = db.Column(db.String(150))
    image = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



