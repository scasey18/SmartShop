from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'Customers'
    custID = db.Column(db.Integer, primary_key=True)
    fName = db.Column(db.String(50))
    lName = db.Column(db.String(50))
    emailAdr = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    def __init__(self, fname, lname, emailAdr, password):
        self.fName = fname
        self.lName = lname
        self.emailAdr = emailAdr
        self.password = password

    def get_id(self):
        return (self.custID)


class Product(db.Model):
    prodID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Numeric(scale=2))
    curinv = db.Column(db.Integer)
    desc = db.Column(db.String(124))

    def __init__(self, name, price, curinv, desc):
        self.name = name
        self.price = price
        self.curinv = curinv
        self.desc = desc


class Address(db.Model):
    adrID = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(50))
    suite = db.Column(db.Integer)
    state = db.Column(db.String(5))
    country = db.Column(db.String(50))
    zip = db.Column(db.Integer)

    def __init__(self, street, suite, state, country, zip):
        self.street = street
        self.suite = suite
        self.state = state
        self.country = country
        self.zip = zip


class Orders(db.Model):
	ordID = db.Column(db.Integer, primary_key=True)
	custID = db.Column(db.Integer)
	prodID = db.Column(db.Integer)
	ShipAdrID = db.Column(db.Integer)
	quantity = db.Column(db.Integer)
	
	def __init__(self, custID, prodID, ShipAdrID, quantity):
		self.custID = custID
		self.prodID = prodID
		self.ShipAdrID = ShipAdrID
		self.quantity = quantity

class Cart(db.Model):
	custID = db.Column(db.Integer, primary_key=True)
	prodID = db.Column(db.Integer, primary_key=True)
	quantity = db.Column(db.Integer)
	
	def init(self, custID, prodID, quantity):
		self.custID = custID
		self.prodID = prodID
		self.quantity = quantity
