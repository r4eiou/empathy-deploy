from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_session import Session

mongo = PyMongo()
bcrypt = Bcrypt()
sess = Session()