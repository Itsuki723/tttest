from sqlalchemy import Select, asc

from models.bookmodel import BookModel
from common.extensions import db

class BookService:
    def get_book_by_id(self,book_id:int):
        return db.session.get(BookModel,book_id)

    def get_book_list(self):
        query = Select(BookModel).order_by(asc(BookModel.name))
        return db.session.scalars(query).all()

    def get_book_by_name(self,book_name:str):
        query = Select(BookModel).where(BookModel.name==book_name)
        return db.session.scalars(query).all()

    def create_book(self,book_model:BookModel):
        exist_book = self.get_book_by_name(book_model.name)
        if exist_book:
            raise Exception(f"book {book_model.name} already exist")
        db.session.add(book_model)
        db.session.commit()

        return book_model

    def update_book(self, new_book:BookModel):
        exist_book = self.get_book_by_id(new_book.id)
        if not exist_book:
            raise Exception(f"book {new_book.name} not exist")
        if new_book.name:
            exist_book.name = new_book.name
        if new_book.author:
            exist_book.author = new_book.author
        if new_book.publish_time:
            exist_book.publish_time = new_book.publish_time

        db.session.commit()

        return exist_book

    def deletebook(self, del_book:BookModel):
        exist_book = self.get_book_by_id(del_book.id)
        if not exist_book:
            raise Exception(f"book {del_book.name} not exist")
        if exist_book:
            db.session.delete(exist_book)

        db.session.commit()

        return del_book