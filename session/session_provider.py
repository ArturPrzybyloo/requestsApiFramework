import base64

import requests
from config import config
from models.user_models import User, TokenViewModel
from requestsUtils.endpoint_builder import EndpointBuilder


class SessionProvider:
    def __init__(self):
        self.user = config.USERNAME
        self.password = config.PASSWORD

    def default_session(self):
        """Returns session with authorization token"""
        session = requests.Session()
        response = session.post(EndpointBuilder.generate_token(), json=User(user_name=self.user,
                                                                            password=self.password).body).json()
        token_created = TokenViewModel.from_json(response)
        encoded = base64.b64encode(f'{config.USERNAME}:{config.PASSWORD}'.encode('ascii'))
        assert token_created.status == "Success"
        session.headers.update({'Authorization': token_created.token})
        session.headers.update({'authorization': f'Basic {encoded.decode()}'})
        return session

    def new_user_session(self, user_name, password, status="Success"):
        """Returns session for newly created user"""
        session = requests.Session()
        user = User(user_name, password).create_user()
        response = session.post(EndpointBuilder.generate_token(), json=User(user_name=user.user_name,
                                                                            password=user.password).body).json()
        token_created = TokenViewModel.from_json(response)
        encoded = base64.b64encode(f'{user_name}:{password}'.encode('ascii'))
        assert token_created.status == status
        if status:
            session.headers.update({'Authorization': token_created.token})
            session.headers.update({'authorization': f'Basic {encoded.decode()}'})
        return session, user.user_id
