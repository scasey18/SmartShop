from tables import *


def removeCustomer(id):
    res = User.query.filter_by(custID=id).first()
    db.session.delete(res)
    db.session.commit()


def addCustomer(fname, lname, email, pwd):
    cust = User(fname, lname, email, pwd)
    db.session.add(cust)
    db.session.commit()


def updateCustomer(id, fname, lname, email, pwd):
    res = User.query.filter_by(custID=id).first()
    res.fName = fname
    res.lName = lname
    res.emailAdr = email
    if pwd != '':
        res.password = pwd
    db.session.commit()


def addProduct(name, price, stock, desc):
    cust = Product(name, price, stock, desc)
    db.session.add(cust)
    db.session.commit()


def removeProduct(id):
	res = Product.query.filter_by(prodID=id).first()
	db.session.delete(res)
	db.session.commit()

def updateProduct(id, name,price,stock,desc):
	res = Product.query.filter_by(prodID=id).first()
	res.name = name
	res.price = price
	res.curinv = stock
	if desc != '':
		res.desc = desc
	db.session.commit()

def addAddress(street, suite, state, country, zip):
	adr = Address(street, suite, state, country, zip)
	db.session.add(adr)
	db.session.commit()

def removeAddress(id):
	adr = Address.query.filter_by(adrID=id).first()
	db.session.delete(adr)
	db.session.commit()

def updateAddress(id, street, suite, state, country, zip):
	adr = Address.query.filter_by(adrID=id).first()
	adr.street=street
	adr.suite=suite
	adr.state = state
	adr.country = country
	adr.zip = zip
	db.session.commit()

def addOrder(custID, prodID, ShipAdrID, quantity):
	ord = Orders(custID, prodID, ShipAdrID, quantity)
	db.session.add(ord)
	db.session.commit()

def removeOrder(id):
	res = Orders.query.filter_by(ordID=id).first()
	db.session.delete(res)
	db.session.commit()

def updateOrder(id, custID, prodID, ShipAdrID, quantity):
	res = Orders.query.filter_by(ordID=id).first()
	res.custID = custID
	res.prodID = prodID
	res.ShipAdrID = ShipAdrID
	res.quantity = quantity
	db.session.commit()