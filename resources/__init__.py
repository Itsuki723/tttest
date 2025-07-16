from flask import Flask
from flask_restful import Api
from flask_apispec import FlaskApiSpec
from flask_sqlalchemy import SQLAlchemy
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
app = Flask(__name__)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:Cnm233@127.0.0.1/testdb'

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Restful API proj',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/',
})

db = SQLAlchemy(app)
docs = FlaskApiSpec(app)

from resources import book_resources
from resources import user_resources