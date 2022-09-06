from config import config


class EndpointBuilder:
    base_account = f'{config.BASE_URL}/Account/{config.API_PATH}'
    base_bookstore = f'{config.BASE_URL}/BookStore/{config.API_PATH}'

    @classmethod
    def create_user(cls):
        return f'{cls.base_account}/User'

    @classmethod
    def generate_token(cls):
        return f'{cls.base_account}/GenerateToken'

    @classmethod
    def get_user_by_id(cls, uuid):
        return f'{cls.base_account}/User/{uuid}'

    @classmethod
    def books(cls):
        return f'{cls.base_bookstore}/Books'

    @classmethod
    def book(cls):
        return f'{cls.base_bookstore}/Book'
