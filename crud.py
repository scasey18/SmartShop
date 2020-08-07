from tables import *

def removeCustomer(id):
    res = getCustomer(id)
    db.session.delete(res)
    db.session.commit()

def getCustomer(id):
	return User.query.filter_by(custID=id).first()

def addCustomer(fname, lname, email, pwd):
    cust = User(fname, lname, email, pwd)
    db.session.add(cust)
    db.session.commit()

def updateCustomer(id, fname, lname, email, pwd):
    res = getCustomer(id)
    res.fName = fname
    res.lName = lname
    res.emailAdr = email
    if pwd != '':
        res.password = pwd
    db.session.commit()

def getRating(prodID):
	return Rating.query.filter(prodID = prodID).first()
	
def getCart(custID):
	return Cart.query.filter_by(custID=custID).all()

def getOrders(id):
	return Orders.query.filter(custID=id).all()

def getProduct(id):
	return Product.query.filter_by(prodID=id).first()

def getAddress(id):
	return Address.query.filter_by(adrID=id).first()

def addProduct(name, price, stock, desc):
    cust = Product(name, price, stock, desc)
    db.session.add(cust)
    db.session.commit()

def removeProduct(id):
	res = getProduct(id)
	db.session.delete(res)
	db.session.commit()

def updateProduct(id, name,price,stock,desc):
	res = getProduct(id)
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
	return adr

def removeAddress(id):
	adr = getAddress(id)
	db.session.delete(adr)
	db.session.commit()

def updateAddress(id, street, suite, state, country, zip):
	adr = getAddress(id)
	adr.street=street
	adr.suite=suite
	adr.state = state
	adr.country = country
	adr.zip = zip
	db.session.commit()

def addOrder(custID, ShipAdrID):
	ord = Orders(custID, ShipAdrID)
	db.session.add(ord)
	db.session.commit()

def removeOrder(id):
	res = getOrders(id)
	db.session.delete(res)
	db.session.commit()

def updateOrder(id, custID, ShipAdrID):
	res = getOrders(id).first()
	res.custID = custID
	res.ShipAdrID = ShipAdrID
	db.session.commit()
	
def addRating(custID,prodID,rating,comment=""):
	res = Rating.query.filter(custID=custID, prodID = prodID).all()
	if res == None:
		db.session.add(Rating(custID,prodID,rating,comment))
		db.session.commit()
		setProdRating(prodID)
		db.session.commit()

def updateRating(custID,prodID,rating,comment=""):
	res = Rating.query.filter(custID=custID, prodID = prodID).all()
	if res != None:
		res.rating=rating
		if comment != "":
			res.comment = comment
	db.session.commit()

def removeRating(custID,prodID):
	res = Rating.query.filter(custID=custID, prodID = prodID).all()
	if res != None:
		db.session.delete(res)
		db.session.commit()