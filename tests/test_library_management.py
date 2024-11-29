import unittest
import os
from unittest.mock import patch, MagicMock
from library.library_management import Library
from library.models import Book


class TestLibrary(unittest.TestCase):
    def setUp(self):
        """
        Set up a temporary library instance and mock the books file.
        """
        self.temp_books_file = "test_books.json"
        self.library = Library(books_file=self.temp_books_file)

    def tearDown(self):
        """
        Clean up the temporary books file after each test.
        """
        if os.path.exists(self.temp_books_file):
            os.remove(self.temp_books_file)

    def test_load_books_empty(self):
        """
        Test loading books when the file doesn't exist or is empty.
        """
        self.assertEqual(len(self.library.books), 0)

    def test_save_books(self):
        """
        Test saving books to the JSON file.
        """
        book = Book(book_id=1, title="Test Book", author="Author", year=2022)
        self.library.books.append(book)
        self.library.save_books()
        self.assertTrue(os.path.exists(self.temp_books_file))
        with open(self.temp_books_file, "r") as file:
            data = file.read()
            self.assertIn("Test Book", data)

    @patch("builtins.input", side_effect=["Test Book", "Author", "2022"])
    def test_add_book(self, mock_input):
        """
        Test adding a new book to the library.
        """
        self.library.add_book()
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Test Book")
        self.assertEqual(self.library.books[0].author, "Author")
        self.assertEqual(self.library.books[0].year, 2022)

    @patch("builtins.input", side_effect=["Duplicate Book", "Author", "2022"])
    def test_add_duplicate_book(self, mock_input):
        """
        Test adding a duplicate book to the library.
        """
        # Add the first book
        book = Book(book_id=1, title="Duplicate Book", author="Author", year=2022)
        self.library.books.append(book)

        # Attempt to add the duplicate
        self.library.add_book()
        self.assertEqual(len(self.library.books), 1)  # Ensure no duplicate was added

    @patch("builtins.input", side_effect=["999"])
    def test_delete_non_existent_book(self, mock_input):
        """
        Test deleting a book that doesn't exist.
        """
        with patch("library.helper_functions.is_library_empty", return_value=False):
            with patch("library.helper_functions.get_valid_id", return_value=999):
                self.library.delete_book()
                self.assertEqual(len(self.library.books), 0)

    @patch("builtins.input", side_effect=["1", "1"])  # Mock book ID and status selection
    def test_change_status(self, mock_input):
        """
        Test changing the status of a book.
        """
        book = Book(book_id=1, title="Test Book", author="Author", year=2022, status="borrowed")
        self.library.books.append(book)
        self.library.change_status()
        self.assertEqual(self.library.books[0].status, "available")

    @patch("builtins.print")
    def test_display_books(self, mock_print):
        """
        Test displaying books in the library.
        """
        self.library.books = [
            Book(book_id=1, title="Книга 1", author="Автор 1", year=2021, status="доступна"),
            Book(book_id=2, title="Книга 2", author="Автор 2", year=2022, status="занята"),
        ]
        self.library.display_books()

        # Verify table header and rows are printed correctly
        mock_print.assert_any_call(f"{'ID':<5} {'Название':<30} {'Автор':<20} {'Год':<6} {'Статус':<10}")
        mock_print.assert_any_call("-" * 75)
        mock_print.assert_any_call(f"{1:<5} {'Книга 1':<30} {'Автор 1':<20} {2021:<6} {'доступна':<10}")
        mock_print.assert_any_call(f"{2:<5} {'Книга 2':<30} {'Автор 2':<20} {2022:<6} {'занята':<10}")

    @patch("builtins.input", side_effect=["2", "Автор 1"])
    @patch("builtins.print")
    def test_search_books(self, mock_print, mock_input):
        """
        Test searching for books by author.
        """
        self.library.books = [
            Book(book_id=1, title="Книга 1", author="Автор 1", year=2021, status="доступна"),
            Book(book_id=2, title="Книга 2", author="Автор 2", year=2022, status="занята"),
        ]
        self.library.search_books()

        # Verify the printed output
        mock_print.assert_any_call("\nНайдено 1 книг(и):")
        mock_print.assert_any_call(f"{'ID':<5} {'Название':<30} {'Автор':<20} {'Год':<6} {'Статус':<10}")
        mock_print.assert_any_call("-" * 75)
        mock_print.assert_any_call(f"{1:<5} {'Книга 1':<30} {'Автор 1':<20} {2021:<6} {'доступна':<10}")


    @patch("builtins.print")
    def test_is_library_empty(self, mock_print):
        """
        Test the behavior when the library is empty.
        """
        self.library.books = []
        self.library.display_books()
        mock_print.assert_any_call("В библиотеке нет книг.")

if __name__ == "__main__":
    unittest.main()