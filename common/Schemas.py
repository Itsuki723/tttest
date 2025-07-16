
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models.bookmodel import BookModel


class TokenSchema(Schema):          #swagger文档token需求
    token = fields.String(required=True)

class BookRequestSchema(Schema):    #swagger文档请求体样板
    name = fields.String(required=True)
    author = fields.String(required=True)
    publish_time = fields.DateTime(required=True)

class BookModelSchema(SQLAlchemyAutoSchema):    #swagger文档返回示例用，返回Bookmodel时用此方法
    class Meta:
        model = BookModel
        load_instance = True