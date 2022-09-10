from faker import Faker

from session.session_provider import SessionProvider


class BaseTest:
    def __init__(self):
        self.fake = Faker('en_US')
        self.session, self.user_id = SessionProvider().new_user_session(self.fake.first_name() + self.fake.last_name(),
                                                              "aaaAAA123@")
