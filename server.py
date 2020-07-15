from flask import Flask, render_template

app = Flask(__name__)


@app.route('/home')
@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/cart')
def getCart():
    return render_template('cart.html')


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


if __name__ == "__main__":
    app.run(debug=True)
