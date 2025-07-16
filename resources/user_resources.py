import jwt
from flask import request
from flask_apispec import MethodResource, doc, use_kwargs
from flask_restful import Resource

from common.Schemas import UserLoginSchema
from common.constants import LOGIN_SECRET
from services.user_services import UserService

class UserResource(MethodResource,Resource):
    @doc(description="user logging", tags=['UserRequest'])
    @use_kwargs(UserLoginSchema,location="json")
    def post(self, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')

        user_model = UserService().login(username, password)
        if user_model:
            user_json = user_model.serialize()
            jwt_token = jwt.encode(user_json, LOGIN_SECRET, algorithm='HS256')
            if isinstance(jwt_token, bytes):
                jwt_token = jwt_token.decode('utf-8')

            user_json['token'] = jwt_token
            return user_json
        else:
            return {'error':'Invalid username or password'},401

