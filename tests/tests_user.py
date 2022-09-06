from faker import Faker

from helpers.status_codes import StatusCodes
from models.user_models import User
from session.session_provider import SessionProvider


class UserTests:
    fake = Faker('en_US')
    session, user_id = SessionProvider().new_user_session(fake.first_name() + fake.last_name(), "aaaAAA123@")

    def test_create_user(self):
        # Get user and verify that he have empty books collection
        user = User.get_user_by_id(self.session, self.user_id)
        assert user.books == []

        # Delete user and verify that he can't be found
        User.delete_user(self.session, user.id)
        response = User.get_user_by_id(self.session, user.id, StatusCodes.UNAUTHORIZED)
        assert response.message == "User not found!"


if __name__ == '__main__':
    UserTests().test_create_user()
