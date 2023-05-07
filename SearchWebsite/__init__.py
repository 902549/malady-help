from logging import NullHandler
from flask import Flask
from sentence_transformers import SentenceTransformer, util
from flask_sqlalchemy import SQLAlchemy
import faiss
from pprint import pprint
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

##secret config key for login safety
app.config['SECRET_KEY'] = 'bbf34737e43416a1318538f507cb100e'

#making a sqllite db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#Instatiating a db instance
db = SQLAlchemy(app)

#for hashing the password
bcrypt = Bcrypt(app)

#instance of loginManager
loginmanager = LoginManager(app)
loginmanager.login_view = 'login'
loginmanager.login_message_category = 'info'
from SearchWebsite import routes