from faker import Faker
from config import config
from models.book_models import Book
from models.user_models import User
from requestsUtils.endpoint_builder import EndpointBuilder
from session.session_provider import SessionProvider



if __name__ == '__main__':
    fake = Faker('en_US')

    session = SessionProvider().default_session()

    user = User(fake.first_name(), "aaaAAA123@").create_user(session)

    # books = Book.get_all_books(session)
    # book = Book.find_book_by_title(books, "Git Pocket Guide")
    book = Book.get_book_by_isbn(session, "9781491950296")
    Book.add_book_to_user(session, config.USER_ID, book.isbn)
    Book.delete_book_from_user(session, user.id, book.isbn)
