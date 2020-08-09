from crud import *
	
def addtoCart(custID, prodID, quantity):
	res = Cart.query.filter_by(custID=custID, prodID=prodID).first()
	prod = Product.query.filter_by(prodID=prodID).first().curinv
	if (res == None):
		if (prod < int(quantity)):
			return -1
		ad = Cart(custID,prodID,quantity)
		db.session.add(ad)
	else:
		if (res.quantity + int(quantity) > prod):
			return -1
		res.quantity += int(quantity)
	db.session.commit()
	return 0

def updateCart(custID, prodID, quantity):
	res = Cart.query.filter_by(custID=custID, prodID=prodID).first()
	prod = Product.query.filter_by(prodID=prodID).first().curinv
	if (quantity > prod):
		return -1
	res.quantity = int(quantity)
	db.session.commit()
	return 0

def removeFromCart(custID,prodID):
	res = Cart.query.filter_by(custID=custID, prodID=prodID).first()
	if (res != None):
		db.session.delete(res)
		db.session.commit()
		
def emptyCart(custID):
	cart = getCart(custID)
	for i in cart:
		db.session.delete(i)
	db.session.commit()

def getCartContents(cart):
	contents = []
	for i in cart:
		contents.append([getProduct(i.prodID), i.quantity])
	return contents
	
def checkoutCart(custID, shipAdrID):
	cart = getCart(custID)
	res = Orders(custID, shipAdrID)
	db.session.add(res)
	db.session.commit()
	contents = []
	for i in cart:
		contents.append(OrderContents(res.ordID,i.prodID,i.quantity))
		Product.query.filter_by(prodID=i.prodID).first().curinv -= i.quantity
	db.session.add_all(contents)
	emptyCart(custID)
	return res
		
def setProdRating(prodID):
	res = getRating(prodID)
	cur = 0
	for i in res:
		cur += i.rating
	Product.query.filter(prodID=prodID).first().rating = cur/len(res)