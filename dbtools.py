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
