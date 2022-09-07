from faker import Faker
import uuid
from helpers.status_codes import StatusCodes
from models.user_models import User
from session.session_provider import SessionProvider
from config import config


class UserTests:
    fake = Faker('en_US')
    session, user_id = SessionProvider().new_user_session(fake.first_name() + fake.last_name(), "aaaAAA123@")

    def test_create_user(self):
        # Get user and verify that he have empty books collection
        user = User.get_user_by_id(self.session, self.user_id)
        assert user.books == []

        # Delete user and verify that he can't be found
        User.delete_user(self.session, user.id)
        response = User.get_user_by_id(self.session, user_id=user.id, status_code=StatusCodes.UNAUTHORIZED)
        assert response.message == "User not found!"

    def test_user_id_validation(self):
        # Get user using random generated UUID
        response = User.get_user_by_id(self.session, user_id=uuid.uuid4(), status_code=StatusCodes.UNAUTHORIZED)
        assert response.message == "User not found!"

        # Delete user using random generated UUID
        # BUG: Delete returns 200 error code with message: User Id not correct!
        response = User.delete_user(self.session, user_id=uuid.uuid4(), status_code=StatusCodes.UNAUTHORIZED)
        assert response.message == "User Id not correct!"

    def test_create_user_with_already_existing_credentials(self):
        # Create user with already registered credentials
        _, response = User(config.USERNAME, config.PASSWORD).create_user(status_code=StatusCodes.NOT_ACCEPTABLE)
        assert response.message == "User exists!"

    def test_user_authorization(self):
        # Try to authorize with correct credentials
        _, response = User(config.USERNAME, config.PASSWORD).authorize(self.session)
        assert response.status == "Success"
        assert response.result == "User authorized successfully."
        assert response.token is not None

        # Try to authorize with incorrect credentials
        _, response = User(self.fake.first_name() + self.fake.last_name(), "test123A@", config.PASSWORD)\
            .authorize(self.session)
        assert response.token is None
        assert response.status == "Failed"
        assert response.result == "User authorization failed."


if __name__ == '__main__':
    UserTests().test_user_authorization()
