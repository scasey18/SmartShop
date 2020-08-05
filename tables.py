from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'Customers'
    custID = db.Column(db.Integer, primary_key=True)
    fName = db.Column(db.Text)
    lName = db.Column(db.Text)
    emailAdr = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    defAdr = db.Column(db.Integer)
    admin = db.Column(db.Integer)

    def __init__(self, fname, lname, emailAdr, password):
        self.fName = fname
        self.lName = lname
        self.emailAdr = emailAdr
        self.password = password
        self.defAdr = 0
        self.admin = 0

    def get_id(self):
        return (self.custID)

    def __repr__(self):
        return f"User { self.custID }, {self.fName} {self.lName}, {self.emailAdr}"


class Product(db.Model):
    prodID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    price = db.Column(db.Numeric(scale=2))
    curinv = db.Column(db.Integer)
    rating = db.Column(db.Float)
    desc = db.Column(db.Text)

    def __init__(self, name, price, curinv, desc):
        self.name = name
        self.price = price
        self.curinv = curinv
        self.desc = desc
        rating = 5.0

    def __repr__(self):
        return f"Product {self.prodID}, {self.name}, Inv:{self.curinv}, {self.price}"


class Address(db.Model):
    adrID = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.Text)
    suite = db.Column(db.Integer)
    state = db.Column(db.Text)
    country = db.Column(db.Text)
    zip = db.Column(db.Integer)

    def __init__(self, street, suite, state, country, zip):
        self.street = street
        self.suite = suite
        self.state = state
        self.country = country
        self.zip = zip

    def __repr__(self):
        return f"Address {self.adrID}: {self.street} {self.suite} {self.state} {self.country} {self.zip}"


class Orders(db.Model):
    ordID = db.Column(db.Integer, primary_key=True)
    custID = db.Column(db.Integer)
    ShipAdrID = db.Column(db.Integer)

    def __init__(self, custID, ShipAdrID):
        self.custID = custID
        self.ShipAdrID = ShipAdrID

    def __repr__(self):
        return f"Order {self.ordID}: {self.custID} {self.ShipAdrID}"


class OrderContents(db.Model):
    ordID = db.Column(db.Integer, primary_key=True)
    prodID = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)

    def __init__(self, ordID, prodID, quantity):
        self.ordID = ordID
        self.prodID = prodID
        self.quantity = quantity

    def __repr__(self):
        return f"Contents {self.ordID}: {self.prodID} x{self.quantity}"


class Cart(db.Model):
    cartid = db.Column(db.Integer, primary_key=True)
    custID = db.Column(db.Integer)
    prodID = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    def __init__(self, custID, prodID, quantity):
        self.custID = custID
        self.prodID = prodID
        self.quantity = quantity

    def __repr__(self):
        return f"Cart {self.custID}: {self.prodID} x{self.quantity}"


class Rating(db.Model):
    rateID = db.Column(db.Integer, primary_key=True)
    custID = db.Column(db.Integer)
    prodID = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)

    def __init__(self, rateID, custID, prodID, rating, comment=""):
        self.rateID = rateID
        self.custID = custID
        self.prodID = prodID
        self.rating = rating
        self.comment = comment

    def __repr__(self):
        return f"Rating ID:{self.rateID}, Customer:{self.custID}, Prod:{self.prodID}, Rating:{self.rating}"
