from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_bcrypt import Bcrypt
import os

auth = HTTPBasicAuth()
bcrypt = Bcrypt()
baseURL = os.getcwd()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e78621be9ed40cbaca8db87bec1adc47'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////{baseURL}/zerocore.db'

db = SQLAlchemy(app)

from crome.models import Client, Credentials
from crome import routes
