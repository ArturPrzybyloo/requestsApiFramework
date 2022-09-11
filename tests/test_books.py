from models.book_models import Book
from models.user_models import User
from tests.base_test import TestBase
from assertpy import assert_that


class TestBooks(TestBase):

    def test_get_all_books(self):
        # Get all books and verify that response not contain empty collection
        books = Book.get_all_books(self.session)
        assert_that(books).is_not_empty()

    def test_add_book_to_user(self):
        # Add book to user and verify that it have been added
        books = Book.get_all_books(self.new_user_session)
        Book.add_book_to_user(self.new_user_session, self.user_id, books[0].isbn)

        user = User.get_user_by_id(self.new_user_session, self.user_id)
        assert_that(user.books[0].isbn).is_equal_to(books[0].isbn)

    def test_delete_book_from_user(self):
        #  Adds and Deletes book from user and verify that it have been deleted
        books = Book.get_all_books(self.new_user_session)
        Book.add_book_to_user(self.new_user_session, self.user_id, books[0].isbn)
        Book.delete_book_from_user(self.new_user_session, self.user_id, books[6].isbn)

        user = User.get_user_by_id(self.new_user_session, self.user_id)
        assert_that(user.books[0].isbn).is_equal_to([])



