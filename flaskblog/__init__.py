from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from cloudant.client import Cloudant

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
client = Cloudant.iam("1f2c0062-950d-4d55-912c-10495ec948e5-bluemix", "PJJTGZh1-XafDMVQ4gmohqjJbuy8mZ8sWzTc68I4WcDt")
client.connect()
my_database = client.create_database("test")
changes = my_database.changes(feed='continuous',since='now',heartbeat=5000,include_docs=True)

from flaskblog import routes

def checkleak(data):
    inlet=data['s1']
    outlet=data['s3']+data['s4']+data['s5']
    if abs(inlet-outlet) > threshold:
        return True
    return False