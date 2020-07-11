from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text


app = Flask(__name__)

db_name = 'sample.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

app.secret_key='CS421'

class Customers(db.Model):
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

class Product(db.Model):
	prodID = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	price = db.Column(db.Numeric)
	curinv = db.Column(db.Integer)
	desc = db.Column(db.String(124))

db.create_all()

@app.route('/')
@app.route('/home')
def homepage():
	return render_template('home.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/admin', methods=['GET','POST'])
def admin():
	if request.method == 'POST':
		print(request.form)
		if request.form['removeCust']:
			db.session.remove(Customers.query().filter_by(id=request.form['removeCust']).all())
		else:
			req = request.form
			cust = Customers(req['fname'],req['lname'],req['email'],req['pwd'])
			db.session.add(cust)
		db.session.commit()
		return render_template("admin.html", customer=Customers.query.all(),products=Product.query.all())
	return render_template("admin.html", customer=Customers.query.all(),products=Product.query.all())

app.run()