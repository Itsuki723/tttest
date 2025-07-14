from datetime import datetime

import jwt
from flask import request
from flask_restful import Resource

from common.api_tools import token_required
from common.constants import LOGIN_SECRET
from models.bookmodel import BookModel
from resources import api

from services.book_services import BookService

class BookResource(Resource):
    def get(self,book_id:int):
        book_model = BookService().get_book_by_id(book_id)
        if book_model:
            return book_model.serialize()
        else:
            return {'error':f'Book not found,id={book_id}'},404
    @token_required
    def put(self,book_id:int):
        try:
            request_json = request.get_json()
            if request_json:
                name = request_json.get('name', None)
                author = request_json.get('author', None)
                publish_time_str = request_json.get('publish_time', None)
                publish_time = datetime.fromisoformat(publish_time_str) if publish_time_str else None

                new_book = BookModel(id = book_id,name = name, author = author, publish_time = publish_time)
                book_service = BookService()
                new_book = book_service.update_book(new_book)

                return new_book.serialize()
            else:
                return {'error':'request body is empty'},400
        except Exception as e:
            return {'error':f'{e}'},400
    @token_required
    def delete(self,book_id:int):
        try:
            book_model = BookService().get_book_by_id(book_id)
            if book_model:
                book_service = BookService()
                book_model = book_service.deletebook(book_model)
                return book_model.serialize()
            else:
                return {'error': f'Book not found,id={book_id}'}, 404
        except Exception as e:
            return {'error': f'{e}'},400

class BookListResource(Resource):
    def get(self):
        book_list = BookService().get_book_list()
        if book_list:
            return [book_model.serialize() for book_model in book_list]
        else:
            return{'error':'no books here'},404
    @token_required
    def post(self):
        try:
            request_json = request.get_json()
            if request_json:
                name = request_json.get('name', None)
                author = request_json.get('author', None)
                publish_time = datetime.fromisoformat(request_json.get('publish_time', None))

                new_book = BookModel(name=name, author=author, publish_time=publish_time)
                book_service = BookService()
                book_service.create_book(new_book)

                return new_book.serialize()
            else:
                return {'error':'request body is empty'},400
        except Exception as e:
            return {'error':f'{e}'},400


api.add_resource(BookResource,'/books/<int:book_id>')
api.add_resource(BookListResource,'/books')