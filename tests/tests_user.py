from faker import Faker

from models.user_models import User
from session.session_provider import SessionProvider


class UserTests:
    fake = Faker('en_US')
    session, user_id = SessionProvider().new_user_session(fake.first_name(), "aaaAAA123@")

    def test_create_user(self):
        user = User.get_user_by_id(self.session, self.user_id)
        assert user.books == []


if __name__ == '__main__':
    UserTests().test_create_user()
