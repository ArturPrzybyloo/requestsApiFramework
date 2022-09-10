from faker import Faker

from session.session_provider import SessionProvider


class TestBase:
    fake = Faker('en_US')
    new_user_session, user_id = SessionProvider().new_user_session(fake.first_name() + fake.last_name(), "aaaAAA123@")
    session = SessionProvider().default_session()

