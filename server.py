from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user

from dbtools import *

app = Flask(__name__)

login = LoginManager(app)

db_name = 'sample.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

db.init_app(app)

with app.app_context():
	db.create_all()

app.secret_key='CS421'

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
		return render_template('home.html', user=current_user)
	return render_template('home.html')
	
@app.route('/signup')
def signup():
	return render_template('signup.html')


@app.route('/cart')
def getCart():
	if current_user.is_authenticated:
		return render_template('cart.html', user=current_user)
	return render_template('cart.html')

@app.route('/store')
def store():
	if current_user.is_authenticated:
		return render_template('store.html', user=current_user)
	return render_template('store.html')

@app.route('/about')
def about():
	if current_user.is_authenticated:
		return render_template('about.html', user=current_user)
	return render_template('about.html')

@app.route('/contact')
def contact():
	if current_user.is_authenticated:
		return render_template('contact.html', user=current_user)
	return render_template('contact.html')

@app.route('/thankyou')
def signup_thankyou():
	return render_template('signup_thankyou.html')


@app.route('/checkout')
def checkout():
	if current_user.is_authenticated:
		return render_template('checkout.html', user=current_user)
	return render_template('checkout.html')


@app.route('/thank_you')
def sales_thankyou():
	if current_user.is_authenticated:
		return render_template('sales_thankyou.html', user=current_user)
	return render_template('sales_thankyou.html')


@app.route('/product')
def product():
	if current_user.is_authenticated:
		return render_template('product.html', user=current_user)
	return render_template('product.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == "POST":
		req = dict(request.form)
		user = User.query.filter_by(emailAdr=req['uname']).first()
		if user.password == req['pwd']:
			login_user(user)
			return redirect(url_for('homepage'))
	return render_template('login.html')

@app.route('/admin', methods=['GET','POST'])
def admin():
	if request.method == 'POST':
		req = dict(request.form)
		print(req)
		if "Customer" in req:
			if req["Customer"] == "Add":
				addCustomer(req['fname'],req['lname'],req['email'],req['pwd'])
			elif req["Customer"] == "Remove":
				deleteCustomer(req['id'])
			elif req["Customer"] == "Update":
				updateCustomer(req['id'],req['fname'],req['lname'],req['email'],req['pwd'])
		elif "Product" in req:
			if req["Product"] == "Add":
				addProduct(req['name'],req['price'],req['stock'],req['desc'])
			elif req["Product"] == "Remove":
				deleteProduct(req['Pid'])
			elif req["Product"] == "Update":
				updateProduct(req['Pid'],req['name'],req['price'],req['stock'],req['desc'])
	return render_template("admin.html", customer=User.query.all(),products=Product.query.all())

app.run()