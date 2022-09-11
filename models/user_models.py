import json

import requests

from helpers.assertion_utils import verify_response_status_code
from helpers.status_codes import StatusCodes
from models.book_models import Book
from models.utils_models import MessageModal, TokenViewModel
from requestsUtils.endpoint_builder import EndpointBuilder


class User:
    def __init__(self, user_name, password, user_id=None):
        self.user_name = user_name
        self.password = password
        self.id = user_id

    @property
    def body(self):
        return {
            "userName": self.user_name,
            "password": self.password
        }

    def create_user(self, status_code=StatusCodes.CREATED):
        """Creates user and return User object with created user id"""
        session = requests.Session()
        response = session.post(EndpointBuilder.create_user(), json=self.body)
        verify_response_status_code(response, status_code)
        if status_code != StatusCodes.CREATED:
            response = MessageModal.from_json(response.json())
        else:
            response = CreateUserResult.from_json(response.json())
            self.id = response.user_id[0]
        return self, response

    def authorize(self, session, status_code=StatusCodes.OK):
        response = session.post(EndpointBuilder.generate_token(), json=self.body)
        verify_response_status_code(response, status_code)
        response = TokenViewModel.from_json(response.json())
        return self, response

    @classmethod
    def get_user_by_id(cls, session, user_id, status_code=StatusCodes.OK):
        """ Finds user by id and returns user object"""
        response = session.get(EndpointBuilder.user_by_id(user_id))
        verify_response_status_code(response, status_code)
        if status_code != StatusCodes.OK:
            response = MessageModal.from_json(response.json())
        else:
            response = GetUserResult.from_json(response.json())
        return response

    @classmethod
    def delete_user(cls, session, user_id, status_code=StatusCodes.OK):
        response = session.delete(EndpointBuilder.user_by_id(user_id))
        verify_response_status_code(response, status_code)
        response = MessageModal.from_json(response.json())
        return response


class CreateUserResult:
    def __init__(self, userID, username, books):
        self.user_id = userID,
        self.username = username
        self.books = books

    @classmethod
    def from_json(cls, json_dict):
        json_string = json.dumps(json_dict)
        json_dict = json.loads(json_string)
        return cls(**json_dict)


class GetUserResult:
    def __init__(self, userId, username, books: list):
        self.id = userId,
        self.username = username
        self.books = books


    @classmethod
    def from_json(cls, json_dict):
        json_string = json.dumps(json_dict)
        json_dict = json.loads(json_string)
        books_objects = []
        for book in json_dict['books']:
            books_objects.append(Book.from_json(book))
        return cls(userId=json_dict['userId'],
                   username=json_dict['username'],
                   books=books_objects)

