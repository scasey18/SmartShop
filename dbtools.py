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


def updateProduct(id, name, price, stock, desc):
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
    adr.street = street
    adr.suite = suite
    adr.state = state
    adr.country = country
    adr.zip = zip
    db.session.commit()


def addOrder(custID, ShipAdrID):
    ord = Orders(custID, ShipAdrID)
    db.session.add(ord)
    db.session.commit()


def removeOrder(id):
    res = Orders.query.filter_by(ordID=id).first()
    db.session.delete(res)
    db.session.commit()


def updateOrder(id, custID, ShipAdrID):
    res = Orders.query.filter_by(ordID=id).first()
    res.custID = custID
    res.ShipAdrID = ShipAdrID
    db.session.commit()


def getOrders(id):
    return Orders.query.filter(custID=id).all()


def addtoCart(custID, prodID, quantity):
    res = Cart.query.filter_by(custID=custID, prodID=prodID).first()
    prod = Product.query.filter_by(prodID=prodID).first().curinv
    if (res == None):
        if (prod < int(quantity)):
            return -1
        ad = Cart(custID, prodID, quantity)
        db.session.add(ad)
    else:
        if (res.quantity + int(quantity) > prod):
            return -1
        res.quantity += int(quantity)
    db.session.commit()
    return 0


def removeFromCart(custID, prodID):
    res = Cart.query.filter_by(custID=custID, prodID=prodID).first()
    if (res != None):
        db.session.delete(res)
        db.session.commit()


def emptyCart(custID):
    cart = getCart(custID)
    for i in cart:
        db.session.delete(i)
    db.session.commit()


def getCart(custID):
    return Cart.query.filter_by(custID=custID).all()


def checkoutCart(custID, shipAdrID):
    cart = getCart(custID)
    res = Orders(custID, shipAdrID)
    db.session.add(res)
    db.session.commit()
    contents = []
    for i in cart:
        contents.append(OrderContents(res.ordID, i.prodID, i.quantity))
        #Product.query.filter(prodID=i.prodID).first().curinv -= i.quantity
    db.session.add_all(contents)
    emptyCart(custID)


def addRating(custID, prodID, rating, comment=""):
    res = Rating.query.filter(custID=custID, prodID=prodID).all()
    if res == None:
        db.session.add(Rating(custID, prodID, rating, comment))
        db.session.commit()
        setProdRating(prodID)
        db.session.commit()


def updateRating(custID, prodID, rating, comment=""):
    res = Rating.query.filter(custID=custID, prodID=prodID).all()
    if res != None:
        res.rating = rating
        if comment != "":
            res.comment = comment
    db.session.commit()


def removeRating(custID, prodID):
    res = Rating.query.filter(custID=custID, prodID=prodID).all()
    if res != None:
        db.session.delete(res)
        db.session.commit()


def setProdRating(prodID):
    res = getRating(prodID)
    cur = 0
    for i in res:
        cur += i.rating
    Product.query.filter(prodID=prodID).first().rating = cur/len(res)


def getRating(prodID):
    return Rating.query.filter(prodID=prodID).all()
