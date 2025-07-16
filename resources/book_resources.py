from datetime import datetime
from flask import request, Response
from flask_apispec import doc, MethodResource, use_kwargs, marshal_with
from flask_restful import Resource
from common.Schemas import BookModelSchema, BookRequestSchema, TokenSchema
from common.api_tools import token_required
from models.bookmodel import BookModel
from resources import api, docs, app
from services.book_services import BookService

class BookResource(MethodResource,Resource):
    @marshal_with(BookModelSchema,code=200)
    @doc(description="get a book's information",tags=['BookRequest'])
    def get(self,book_id:int):
        book_model = BookService().get_book_by_id(book_id)
        if book_model:
            return book_model,200
        else:
            return {'error':f'Book not found,id={book_id}'},404

    @doc(description="update a book's information", tags=['BookRequest'])
    @use_kwargs(BookRequestSchema,location='json')
    @use_kwargs(TokenSchema,location='headers')
    @marshal_with(BookModelSchema,code=200)
    @token_required
    def put(self,book_id:int,**kwargs):
        try:
            name = kwargs.get('name', None)
            author = kwargs.get('author', None)
            publish_time = kwargs.get('publish_time', None)

            new_book = BookModel(id = book_id,name = name, author = author, publish_time = publish_time)
            book_service = BookService()
            new_book = book_service.update_book(new_book)

            return new_book,200
        except Exception as e:
            return {'error':f'{e}'},400

    @doc(description="delete a book", tags=['BookRequest'])
    @use_kwargs(TokenSchema,location='json')
    @marshal_with(BookModelSchema,code=200)
    @token_required
    def delete(self,book_id:int):
        try:
            book_model = BookService().get_book_by_id(book_id)
            if book_model:
                book_service = BookService()
                book_model = book_service.deletebook(book_model)
                return book_model
            else:
                return {'error': f'Book not found,id={book_id}'}, 404
        except Exception as e:
            return {'error': f'{e}'},400

class BookListResource(MethodResource,Resource):
    @doc(description="get all book's information", tags=['BookRequest'])
    @marshal_with(BookModelSchema,code=200)
    def get(self):
        book_list = BookService().get_book_list()
        if book_list:
            return [book_model for book_model in book_list]
        else:
            return{'error':'no books here'},404

    @doc(description="create a new book", tags=['BookRequest'])
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
docs.register(BookResource)

api.add_resource(BookListResource,'/books')
docs.register(BookListResource)

@app.route('/swagger.yaml')
def generate_swagger_yaml():
    yaml_doc = docs.spec.to_yaml()
    return Response(yaml_doc, mimetype='text/x-yaml')