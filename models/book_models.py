import json

from helpers.assertion_utils import verify_response_status_code
from helpers.status_codes import StatusCodes
from models import user_models
from models.utils_models import MessageModal
from requestsUtils.endpoint_builder import EndpointBuilder


class Book:
    def __init__(self, isbn, title, subTitle, author, publish_date, publisher, pages, description, website):
        self.isbn = isbn
        self.title = title
        self.sub_title = subTitle
        self.author = author
        self.publish_date = publish_date
        self.publisher = publisher
        self.pages = pages
        self.description = description
        self.website = website

    @classmethod
    def from_json(cls, json_dict):
        json_string = json.dumps(json_dict)
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    @classmethod
    def get_all_books(cls, session):
        """ Get all books and returns list of Book objects"""
        response = session.get(EndpointBuilder.books())
        verify_response_status_code(response, StatusCodes.OK)
        books = []
        for book in response.json()['books']:
            added_book = cls.from_json(book)
            books.append(added_book)
        return books

    @classmethod
    def find_book_by_title(cls, all_books: list, title: str):
        """ Finds book by title and return Book object"""
        for book in all_books:
            if title in book.title:
                return book

    @classmethod
    def get_book_by_isbn(cls, session, isbn: str):
        """ Finds book by ISBN and return Book object"""
        response = session.get(EndpointBuilder.book(), params={"ISBN": isbn})
        verify_response_status_code(response, StatusCodes.OK)
        return cls.from_json(response.json())

    @classmethod
    def add_book_to_user(cls, session, user_id, isbn, status_code=StatusCodes.CREATED):
        add_book = {
            "userId": user_id,
            "collectionOfIsbns": [
                {
                    "isbn": isbn
                }
            ]
        }
        response = session.post(EndpointBuilder.books(), json=add_book)
        verify_response_status_code(response, status_code)
        if status_code != StatusCodes.CREATED:
            response = MessageModal.from_json(response.json())
        return response

    @classmethod
    def delete_book_from_user(cls, session, user_id, isbn, status_code=StatusCodes.NO_CONTENT):
        delete_book = {
            "isbn": isbn,
            "userId": user_id
        }
        response = session.delete(EndpointBuilder.book(), json=delete_book)
        verify_response_status_code(response, status_code)
        if status_code != StatusCodes.NO_CONTENT:
            response = MessageModal.from_json(response.json())
        return response
