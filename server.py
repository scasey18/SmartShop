from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from flask_login import LoginManager, UserMixin, current_user, login_user

app = Flask(__name__)

login = LoginManager(app)

db_name = 'sample.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
	__tablename__ = 'Customers'
	custID = db.Column(db.Integer, primary_key=True)
	fName = db.Column(db.String(50))
	lName = db.Column(db.String(50))
	emailAdr = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(50))
	
	def __init__(self, fname,lname,emailAdr,password):
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

db.create_all()

app.secret_key='CS421'

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/home')
@app.route('/')
def homepage():
	if current_user.is_authenticated:
		return render_template('home.html', data=current_user)
	return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == "POST":
			req = dict(request.form)
			user = User.query.filter_by(emailAdr=req['uname']).first()
			if user.password == req['pwd']:
				login_user(user)
				return redirect(url_for('homepage'))
	return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/cart')
def getCart():
    return render_template('cart.html')

@app.route('/store')
def store():
    return render_template('store.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/thankyou')
def signup_thankyou():
    return render_template('signup_thankyou.html')


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/thank_you')
def sales_thankyou():
    return render_template('sales_thankyou.html')


@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/admin', methods=['GET','POST'])
def admin():
	if request.method == 'POST':
		req = dict(request.form)
		print(req)
		if "Customer" in req:
			if req["Customer"] == "Add":
				cust = User(req['fname'],req['lname'],req['email'],req['pwd'])
				db.session.add(cust)
			elif req["Customer"] == "Remove":
				res = User.query.filter_by(custID=req["id"]).first()
				db.session.delete(res)
			elif req["Customer"] == "Update":
				res = User.query.filter_by(custID=req["id"]).first()
				res.fName = req['fname']
				res.lName = req['lname']
				res.emailAdr = req['email']
				if str(req['pwd']) != '':
					res.password = req['pwd']
		elif "Product" in req:
			if req["Product"] == "Add":
				cust = Product(req['name'],req['price'],req['stock'],req['desc'])
				db.session.add(cust)
			elif req["Product"] == "Remove":
				res = Product.query.filter_by(prodID=req["id"]).first()
				db.session.delete(res)
			elif req["Product"] == "Update":
				res = Product.query.filter_by(prodID=req["Pid"]).first()
				res.name = req['name']
				res.price = req['price']
				res.curinv = req['stock']
				if req['desc'] != '':
					res.desc = req['desc']
		db.session.commit()
	return render_template("admin.html", customer=User.query.all(),products=Product.query.all())

if __name__ == "__main__":
    app.run(debug=True)