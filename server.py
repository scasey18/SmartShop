from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_user

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

app.secret_key='CS421'

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
@app.route('/home')
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

app.run()