import unittest
from datetime import datetime
from unittest import mock
from library.models import Book
from library.helper_functions import (
    get_valid_id,
    get_valid_year,
    get_valid_status,
    get_search_choice,
    get_non_empty_string,
    filter_books,
    is_library_empty,
)

class TestHelperFunctions(unittest.TestCase):
    def setUp(self):
        """Set up sample data for testing."""
        self.books = [
            Book(1, "Book One", "Author One", 2001, "available"),
            Book(2, "Book Two", "Author Two", 2002, "borrowed"),
        ]

    def test_is_library_empty(self):
        """Test is_library_empty with empty and non-empty libraries."""
        self.assertTrue(is_library_empty([]), "Should return True for an empty library.")
        self.assertFalse(is_library_empty(self.books), "Should return False for a non-empty library.")

    def test_filter_books(self):
        """Test filtering books by title, author, and year."""
        # Filter by title
        result = filter_books(self.books, "title", "book one")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "Book One")

        # Filter by author
        result = filter_books(self.books, "author", "author two")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].author, "Author Two")

        # Filter by year
        result = filter_books(self.books, "year", "2001")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].year, 2001)

        # No results
        result = filter_books(self.books, "title", "non-existent")
        self.assertEqual(len(result), 0)

    def test_get_non_empty_string(self):
        """Test get_non_empty_string with mock input."""
        with mock.patch("builtins.input", return_value="Test String"):
            self.assertEqual(get_non_empty_string("Enter a string: "), "Test String")

        with mock.patch("builtins.input", side_effect=["", "Valid String"]):
            self.assertEqual(get_non_empty_string("Enter a string: "), "Valid String")

    def test_get_valid_status(self):
        """Test get_valid_status with mock input."""
        with mock.patch("builtins.input", return_value="1"):
            self.assertEqual(get_valid_status(), "available")

        with mock.patch("builtins.input", return_value="2"):
            self.assertEqual(get_valid_status(), "borrowed")

    def test_get_valid_year(self):
        """Test get_valid_year with mock input."""
        current_year = datetime.now().year
        with mock.patch("builtins.input", return_value=str(current_year)):
            self.assertEqual(get_valid_year(), current_year)

        with mock.patch("builtins.input", side_effect=["-1", "3000", "2020"]):
            self.assertEqual(get_valid_year(), 2020)

    def test_get_search_choice(self):
        """Test get_search_choice with mock input."""
        with mock.patch("builtins.input", return_value="1"):
            self.assertEqual(get_search_choice(), "title")

        with mock.patch("builtins.input", return_value="2"):
            self.assertEqual(get_search_choice(), "author")

        with mock.patch("builtins.input", return_value="3"):
            self.assertEqual(get_search_choice(), "year")

    def test_get_valid_id(self):
        """Test get_valid_id with mock input."""
        with mock.patch("builtins.input", return_value="1"):
            self.assertEqual(get_valid_id(self.books), 1)

        with mock.patch("builtins.input", side_effect=["999", "2"]):
            self.assertEqual(get_valid_id(self.books), 2)


if __name__ == "__main__":
    unittest.main()
