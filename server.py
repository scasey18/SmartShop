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


if __name__ == "__main__":
    app.run(debug=True)
