# from operator import add
import os
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

from forms import SubmitAddressForm

app = Flask(__name__)
csrf = CSRFProtect(app)

# adding secret key to use csrf
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# setting the environments and configuring databases for the different environments
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/user_addresses'

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User_Addresses(db.Model):
    __tablename__ = 'ethereum_addresses'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, unique=True)

db.create_all()

def __init__(self, address=""):
    self.address = address

@app.route('/')
def hello():
    return render_template("home.htm")


@app.route("/submit", methods=["POST", "GET"])
def submit_address():
    if request.method == 'POST':
        address = request.form['address']


        if len(address) < 6 or len(address) > 64:
            return render_template("home.htm", message="Invalid address")

        if db.session.query(User_Addresses).filter(User_Addresses.address == address).count() == 0:
            new_address = User_Addresses(address=address)
            print(new_address)
            db.session.add(new_address)
            db.session.commit()
            return render_template("submitted.htm")

        else:
            return render_template("oops.htm")
    return render_template("submitted.htm")

if __name__ == '__main__':
    app.run()