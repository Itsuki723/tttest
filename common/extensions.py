from flask_restful import Api
from flask_apispec import FlaskApiSpec
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
api = Api()
docs = FlaskApiSpec()