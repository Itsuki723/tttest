from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models.bookmodel import BookModel
from models.usermodel import UserModel

class TokenSchema(Schema):          #swagger文档token需求
    token = fields.String(required=True)

class BookRequestSchema(Schema):    #swagger文档数据校验
    name = fields.String(required=True)
    author = fields.String(required=True)
    publish_time = fields.DateTime(required=True)

class BookModelSchema(SQLAlchemyAutoSchema):    #swagger文档返回示例用，返回Bookmodel时用此方法
    class Meta:
        model = BookModel
        load_instance = True

class UserRegisterSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

class UserLoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)