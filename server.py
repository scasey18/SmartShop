from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_user, logout_user

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,  SelectField

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
    if request.method == "POST":
        removeFromCart(current_user.get_id(), request.form.get('remove'))
    if current_user.is_authenticated:
        cart = getCart(current_user.get_id())
        prods = []
        for i in cart:
            prods.append(Product.query.filter_by(prodID=i.prodID).first())
        return render_template('cart.html', user=current_user, cart=len(cart), contents=cart, prods=prods)
    return render_template('cart.html')


# @app.route('/store', methods=['GET', 'POST'])
# def store():
#     if request.method == "POST":
#         req = dict(request.form)
#         res = addtoCart(current_user.get_id(), req['id'], req['quan'])
#         if res == -1:
#             return str(-1)
#         return str(len(getCart(current_user.get_id())))
#     if current_user.is_authenticated:
#         prods = Product.query.all()
#         return render_template('store.html', user=current_user, products=prods, cart=len(getCart(current_user.get_id())))
#     return render_template('store.html', products=Product.query.all())


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
            checkoutCart(current_user.get_id(), 1)
            return redirect(url_for('sales_thankyou'))
        cart = getCart(current_user.get_id())
        return render_template('checkout.html', user=current_user, cart=len(cart), content=cart)
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


@ app.route('/product/<int:prodID>')
def product(prodID):
    if current_user.is_authenticated:
        return render_template('product.html', prod=Product.query.get(prodID))

    return render_template('product.html', prod=Product.query.get(prodID))


@ app.route('/login', methods=['GET', 'POST'])
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


@ app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        req = dict(request.form)
        if "Customer" in req:
            if req["Customer"] == "Add":
                addCustomer(req['fname'], req['lname'], req['email'], req['pwd'])
            elif req["Customer"] == "Remove":
                deleteCustomer(req['id'])
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


@ app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == "POST" and current_user.is_authenticated:
        req = dict(request.form)
        updateCustomer(current_user.get_id(), req['fName'], req['lName'], req['email'], req['pwd'])
    if current_user.is_authenticated:
        return render_template('account.html', user=current_user, cart=len(getCart(current_user.get_id())))
    return redirect(url_for('login'))


@ app.errorhandler(404)
def error404(error):
    if current_user.is_authenticated:
        return render_template('404.html', user=current_user, cart=len(getCart(current_user.get_id())))
    return render_template('404.html')


if __name__ == "__main__":
    app.run(debug=True)
