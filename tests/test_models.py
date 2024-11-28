import unittest
from library.models import Book


class TestBook(unittest.TestCase):
    def test_book_initialization(self):
        """
        Test initializing a Book instance.
        """
        book = Book(book_id=1, title="1984", author="George Orwell", year=1949, status="available")
        
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "1984")
        self.assertEqual(book.author, "George Orwell")
        self.assertEqual(book.year, 1949)
        self.assertEqual(book.status, "available")

    def test_to_dict(self):
        """
        Test the to_dict method of the Book class.
        """
        book = Book(book_id=2, title="Animal Farm", author="George Orwell", year=1945, status="borrowed")
        book_dict = book.to_dict()
        
        expected_dict = {
            "id": 2,
            "title": "Animal Farm",
            "author": "George Orwell",
            "year": 1945,
            "status": "borrowed"
        }
        self.assertEqual(book_dict, expected_dict)

    def test_from_dict(self):
        """
        Test the from_dict static method of the Book class.
        """
        book_data = {
            "id": 3,
            "title": "Brave New World",
            "author": "Aldous Huxley",
            "year": 1932,
            "status": "available"
        }
        book = Book.from_dict(book_data)
        
        self.assertEqual(book.id, 3)
        self.assertEqual(book.title, "Brave New World")
        self.assertEqual(book.author, "Aldous Huxley")
        self.assertEqual(book.year, 1932)
        self.assertEqual(book.status, "available")

    def test_default_status(self):
        """
        Test the default status of a Book instance.
        """
        book = Book(book_id=4, title="The Catcher in the Rye", author="J.D. Salinger", year=1951)
        
        self.assertEqual(book.status, "available")


if __name__ == "__main__":
    unittest.main()