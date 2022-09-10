import uuid
from helpers.status_codes import StatusCodes
from models.user_models import User
from config import config
from assertpy import assert_that

from tests.base_test import TestBase


class TestUsers(TestBase):
    def test_create_user(self):
        # Get user and verify that he have empty books collection
        user = User.get_user_by_id(self.session, self.user_id)
        assert_that(user.books).is_equal_to([])

        # Delete user and verify that he can't be found
        User.delete_user(self.session, user.id)
        response = User.get_user_by_id(self.session, user_id=user.id, status_code=StatusCodes.UNAUTHORIZED)
        assert_that(response.message).is_equal_to("User not found!")

    def test_user_id_validation(self):
        # Get user using random generated UUID
        response = User.get_user_by_id(self.session, user_id=uuid.uuid4(), status_code=StatusCodes.UNAUTHORIZED)
        assert_that(response.message).is_equal_to("User not found!")

        # Delete user using random generated UUID
        # BUG: Delete returns 200 error code with message: User Id not correct!
        response = User.delete_user(self.session, user_id=uuid.uuid4(), status_code=StatusCodes.UNAUTHORIZED)
        assert_that(response.message).is_equal_to("User Id not correct!")

    def test_create_user_with_already_existing_credentials(self):
        # Create user with already registered credentials
        _, response = User(config.USERNAME, config.PASSWORD).create_user(status_code=StatusCodes.NOT_ACCEPTABLE)
        assert_that(response.message).is_equal_to("User exists!")

    def test_user_authorization(self):
        # Try to authorize with correct credentials
        _, response = User(config.USERNAME, config.PASSWORD).authorize(self.session)
        assert_that(response.status).is_equal_to("Success")
        assert_that(response.result).is_equal_to("User authorized successfully.")
        assert_that(response.token).is_not_none()

        # Try to authorize with incorrect credentials
        _, response = User(self.fake.first_name() + self.fake.last_name(), "test123A@", config.PASSWORD)\
            .authorize(self.session)
        assert_that(response.status).is_equal_to("Failed")
        assert_that(response.result).is_equal_to("User authorization failed.")
        assert_that(response.token).is_none()