import jwt
from flask_apispec import MethodResource, doc, use_kwargs
from flask_restful import Resource, marshal_with

from common.Schemas import UserLoginSchema, UserRegisterSchema
from common.constants import LOGIN_SECRET
from services.user_services import UserService

class LoginResource(MethodResource,Resource):
    @doc(description="user logging", tags=['LoginRequest'])
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

class RegisterResource(MethodResource,Resource):
    @doc(description="user registration", tags=['RegisterRequest'])
    @use_kwargs(UserRegisterSchema(),location="json")     #参数解析和校验
    def post(self, **kwargs):
        try:
            user_service = UserService()
            user = user_service.register_user(**kwargs)
            return user.serialize(),201
        except Exception as e:
            return {'error':str(e)},400
