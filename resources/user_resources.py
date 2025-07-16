import jwt
from flask import request
from flask_apispec import MethodResource
from flask_restful import Resource

from common.constants import LOGIN_SECRET
from resources import api,docs
from services.user_services import UserService


class LoginResource(MethodResource,Resource):
    def post(self):
        try:
            request_json = request.json
            if request_json:
                username = request_json.get('username',None)
                password = request_json.get('password',None)

                user_model = UserService().login(username, password)
                if user_model:
                    user_json = user_model.serialize()
                    jwt_token = jwt.encode(user_json, LOGIN_SECRET, algorithms='HS256')
                    user_json['token'] = jwt_token
                    return user_json
                else:
                    return {'error':'Invalid username or password'},401
            else:
                return {'error':'please provide username and password info as JSON'},400
        except Exception as e:
            return {'error':f'{e}'},400
api.add_resource(LoginResource,'/login')
docs.register(LoginResource)