from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,  SelectField

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from dbtools import *
from tables import *

app = Flask(__name__)

login = LoginManager(app)


db_name = 'sample.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

db.init_app(app)

with app.app_context():
	db.create_all()

app.secret_key = 'CS421'


@login.user_loader
def load_user(user_id):
	return User.query.get(user_id)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('homepage'))


@app.route('/')
@app.route('/home')
def homepage():
	if current_user.is_authenticated:
		return render_template('home.html', user=current_user, cart=len(getCart(current_user.get_id())))
	return render_template('home.html')


@app.route('/cart', methods=['GET', 'POST'])
def cart():
	if request.method=="POST":
		req=dict(request.form)
		if "remove" in req:
			removeFromCart(current_user.get_id(),req['remove'])
		else:
			k = list(req.keys())[0]
			updateCart(current_user.get_id(), k, int(req[k]))
	if current_user.is_authenticated:
		cart=getCart(current_user.get_id())
		prods=[]
		for i in cart:
			prods.append(Product.query.filter_by(prodID=i.prodID).first())
		return render_template('cart.html', user=current_user, cart=len(cart), contents=cart, prods=prods)
	return render_template('cart.html')

@app.route('/about')
def about():
	if current_user.is_authenticated:
		return render_template('about.html', user=current_user, cart=len(getCart(current_user.get_id())))
	return render_template('about.html')


@app.route('/contact')
def contact():
	if current_user.is_authenticated:
		return render_template('contact.html', user=current_user, cart=len(getCart(current_user.get_id())))
	return render_template('contact.html')


@app.route('/thankyou')
def signup_thankyou():
	return render_template('signup_thankyou.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for("homepage"))
	error = None
	if request.method == "POST":
		req = dict(request.form)
		user = User.query.filter_by(emailAdr=req['email']).first()
		if (user != None):
			error = "Email address already in use"
		elif (req['pwd'] != req['cpwd']):
			error = "Passwords entered are not the same"
		else:
			addCustomer(req['fName'], req['lName'], req['email'], req['pwd'])
			return redirect(url_for('signup_thankyou'))
		return render_template('signup.html', error=error)
	return render_template('signup.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
	if current_user.is_authenticated:
		if request.method == "POST":
			req = dict(request.form)
			adr = addAddress(req['street'],req['suite'],req['state'], req['country'],req['zip'])
			if "saveAddress" in req and req['saveAddress'] == 'on':
				current_user.defAdr = adr.adrID
				db.session.commit()
			res = checkoutCart(current_user.get_id(), adr.adrID)
			sender = 'shopsmartcs421@gmail.com'
			customer_email = current_user.emailAdr
			customer_name = current_user.fName
			customer_address = Address.query.get(adr.adrID).street
			msg = MIMEMultipart()
			msg['From'] = sender
			msg['To'] = customer_email
			msg['Subject'] = 'Order Confirmation'
			body = "Hi {0}! Thank you for your purchase.\nGood news! Your order was successfully placed! Your order will ship to {1}. Your confirmation number is {2}.\nThank you for Shopping with us and please come back again!".format(customer_name, customer_address, res.confirmNum)
			msg.attach(MIMEText(body, 'html'))
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(sender, "Sh0pSm@rT")
			server.sendmail(sender, customer_email, msg.as_string())
			return redirect(url_for('sales_thankyou'))
		cart = getCart(current_user.get_id())
		return render_template('checkout.html', user=current_user, adr=getAddress(current_user.defAdr), cart=len(cart), content = getCartContents(cart))
	return render_template('checkout.html')

@app.route('/thank_you')
def sales_thankyou():
	if current_user.is_authenticated:
		return render_template('sales_thankyou.html', user=current_user, cart=len(getCart(current_user.get_id())))
	return render_template('sales_thankyou.html')

@app.route('/store', methods=['GET', 'POST'])
def store():
    if request.method == "POST":
        req = dict(request.form)
        res = addtoCart(current_user.get_id(), req['id'], req['quan'])
        if res == -1:
            return str(-1)
        return str(len(getCart(current_user.get_id())))
        if current_user.is_authenticated:
            prods = Product.query.all()
            return render_template('store.html', user=current_user, products=prods, cart=len(getCart(current_user.get_id())))
    else:
        if request.args.get('item') == "filter":
            selectValue = request.args.get("myitems")
            if selectValue != "All":
                prods = Product.query.filter(Product.name == selectValue).all()
                return render_template('store.html', user=current_user, products=prods, cart=len(getCart(current_user.get_id())))
            else:
                prods = Product.query.all()
                return render_template('store.html', user=current_user, products=prods, cart=len(getCart(current_user.get_id())))
    return render_template('store.html', products=Product.query.all())

@app.route('/product/<int:prodID>', methods=['GET', 'POST'])
def product(prodID):
	if current_user.is_authenticated:
		return render_template('product.html', prod=Product.query.get(prodID),ratings=getAllRatings(prodID), user=current_user, cart=len(getCart(current_user.get_id())))
	return render_template('product.html', prod=Product.query.get(prodID), ratings=getAllRatings(prodID))


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('account'))
	if request.method == "POST":
		req = dict(request.form)
		print(req)
		user = User.query.filter_by(emailAdr=req['uname']).first()
		if (user == None or user.password != req['pwd']):
			return render_template('login.html', error="Invalid username or password")
		elif 'remember' in req and req['remember'] == 'on':
			login_user(user, remember=True)
		else:
			login_user(user)
		return redirect(url_for('homepage'))
	return render_template('login.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
	if request.method == 'POST':
		req = dict(request.form)
		if "Customer" in req:
			if req["Customer"] == "Add":
				addCustomer(req['fname'], req['lname'], req['email'], req['pwd'])
			elif req["Customer"] == "Remove":
				removeCustomer(req['id'])
			elif req["Customer"] == "Update":
				updateCustomer(req['id'], req['fname'], req['lname'], req['email'], req['pwd'])
		elif "Product" in req:
			if req["Product"] == "Add":
				addProduct(req['name'], req['price'], req['stock'], req['desc'])
			elif req["Product"] == "Remove":
				deleteProduct(req['Pid'])
			elif req["Product"] == "Update":
				updateProduct(req['Pid'], req['name'], req['price'], req['stock'], req['desc'])
	if current_user.is_authenticated:
		if current_user.admin == 1:
			return render_template("admin.html", customer=User.query.all(), products=Product.query.all())
		else:
			return "Account does not have access"
	return redirect(url_for('login'))


@app.route('/account', methods=['GET', 'POST'])
def account():
	if request.method == "POST" and current_user.is_authenticated:
		req = dict(request.form)
		print(req)
		if "fName" in req:
			updateCustomer(current_user.get_id(), req['fName'], req['lName'], req['email'], req['pwd'])
		elif "reset" in req and req["reset"] == "address":
			current_user.defAdr = 0
			db.session.commit()
		elif "update" in req and req["update"] == "address":
			res = Address.query.filter_by(street=req["street"], suite=req["suite"], state=req["state"],zip=req["zip"]).first()
			if res != None:
				current_user.defAdr = res.adrID
				db.session.commit()
			else:
				adr = addAddress(req["street"],req["suite"],req["state"],"United States",req["zip"])
				current_user.defAdr = adr.adrID
				db.session.commit()
	if current_user.is_authenticated:
		return render_template('account.html', user=current_user, adr=getAddress(current_user.defAdr),cart=len(getCart(current_user.get_id())))
	return redirect(url_for('login'))


@app.errorhandler(404)
def error404(error):
	if current_user.is_authenticated:
		return render_template('404.html', user=current_user, cart=len(getCart(current_user.get_id())))
	return render_template('404.html')


if __name__ == "__main__":
	app.run(debug=True)
