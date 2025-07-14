from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:Cnm233@127.0.0.1/testdb'
db = SQLAlchemy(app)

from resources import  book_resources
from resources import user_resources