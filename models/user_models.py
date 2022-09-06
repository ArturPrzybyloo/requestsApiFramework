import json

import requests

from helpers.assertion_utils import verify_response_status_code
from helpers.status_codes import StatusCodes
from models.book_models import Book
from requestsUtils.endpoint_builder import EndpointBuilder


class User:
    def __init__(self, user_name, password, user_id=None):
        self.user_name = user_name
        self.password = password
        self.user_id = user_id

    @property
    def body(self):
        return {
            "userName": self.user_name,
            "password": self.password
        }

    def create_user(self):
        """Creates user and return User object with created user id"""
        session = requests.Session()
        response = session.post(EndpointBuilder.create_user(), json=self.body)
        verify_response_status_code(response, StatusCodes.CREATED)
        user_register = CreateUserResult.from_json(response.json())
        self.user_id = user_register.user_id[0]
        return self

    @classmethod
    def get_user_by_id(cls, session, user_id):
        """ Finds user by id and returns user object"""
        response = session.get(EndpointBuilder.get_user_by_id(user_id))
        verify_response_status_code(response, StatusCodes.OK)
        get_user = GetUserResult.from_json(response.json())
        return get_user


class TokenViewModel:
    def __init__(self, token, expires, status, result):
        self.token = token
        self.expire = expires
        self.status = status
        self.result = result

    @classmethod
    def from_json(cls, json_dict):
        json_string = json.dumps(json_dict)
        json_dict = json.loads(json_string)
        return cls(**json_dict)


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
    def __init__(self, userId, username, books):
        self.user_id = userId,
        self.username = username
        self.books = books

    @classmethod
    def from_json(cls, json_dict):
        json_string = json.dumps(json_dict)
        json_dict = json.loads(json_string)
        return cls(**json_dict)
