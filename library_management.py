import json
import os
import logging
from models import Book
import helper_functions

class Library:
    def __init__(self, books_file: str = "books.json"):
        """
        Initialize the Library instance.

        Args:
            books_file (str): Path to the file where books data is stored.
        """
        self.books_file = books_file
        self.books = self.load_books()

    # --- File Operations ---
    def load_books(self) -> list[Book]:
        """
        Load books from the JSON file.

        Returns:
            list[Book]: A list of Book objects.
        """
        if os.path.exists(self.books_file):
            try:
                with open(self.books_file, "r") as file:
                    books_data = json.load(file)
                    return [Book.from_dict(book) for book in books_data]
            except json.JSONDecodeError:
                error_message = "Error: books.json is corrupted. Starting with an empty library."
                print(error_message)
                logging.error(error_message)
                return []  # Empty list if file is corrupted
            except Exception as e:
                error_message = f"Unexpected error while loading books: {e}"
                print(error_message)
                logging.error(error_message)
                return []
        else:
            warning_message = "Warning: books.json file not found. A new file will be created."
            print(warning_message)
            logging.warning(warning_message)
            return []

    def save_books(self) -> None:
        """
        Save books to the JSON file.
        """
        try:
            with open(self.books_file, "w") as file:
                json.dump([book.to_dict() for book in self.books], file, indent=4)
        except IOError as e:
            error_message = f"Error: Unable to save books to {self.books_file}. {e}"
            print(error_message)
            logging.error(error_message)
        except Exception as e:
            error_message = f"Unexpected error while saving books: {e}"
            print(error_message)
            logging.error(error_message)

    # --- Core Operations ---
    def add_book(self) -> None:
        """
        Add a new book to the library.
        """
        try:
            title = helper_functions.get_non_empty_string("Enter book title: ")
            author = helper_functions.get_non_empty_string("Enter book author: ")
            year = helper_functions.get_valid_year()

            # Generate a unique ID
            book_id = 1 if not self.books else max(book.id for book in self.books) + 1

            # Create and add the book
            new_book = Book(book_id, title, author, year)
            self.books.append(new_book)
            self.save_books()
            print(f"Book '{title}' added successfully!")
        except Exception as e:
            logging.error(f"Unexpected error while adding a book: {e}")
            print("An unexpected error occurred while adding the book.")

    def delete_book(self) -> None:
        """
        Delete a book from the library by ID.
        """
        try:
            if helper_functions.is_library_empty(self.books):
                return

            book_id = helper_functions.get_valid_id(self.books)
            book_to_delete = next(book for book in self.books if book.id == book_id)
            self.books.remove(book_to_delete)
            self.save_books()
            print(f"Book ID {book_id} deleted successfully.")
        except Exception as e:
            logging.error(f"Unexpected error while deleting a book: {e}")
            print("An unexpected error occurred while deleting the book.")

    def search_books(self) -> None:
        """
        Search for books by title, author, or year.
        """
        try:
            if helper_functions.is_library_empty(self.books):
                return

            # Get the search type
            search_type = helper_functions.get_search_choice()
            
            # Use get_non_empty_string to ensure a valid search query
            search_query = helper_functions.get_non_empty_string(f"Enter {search_type}: ").lower()

            # Filter books based on the search criteria
            matching_books = helper_functions.filter_books(self.books, search_type, search_query)

            if matching_books:
                print(f"\nFound {len(matching_books)} book(s):")
                
                # Print table header for search results
                print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'Year':<6} {'Status':<10}")
                print("-" * 75)
                
                # Print each matching book's details
                for book in matching_books:
                    print(f"{book.id:<5} {book.title:<30} {book.author:<20} {book.year:<6} {book.status:<10}")
            else:
                print("\nNo matching books found.")
                logging.info(f"Search performed: Type='{search_type}', Query='{search_query}', Results=0")
        except Exception as e:
            logging.error(f"Unexpected error while searching for books: {e}")
            print("An unexpected error occurred while searching for books.")

    def display_books(self) -> None:
        """
        Display all books in the library in a tabular format.
        """
        try:
            if helper_functions.is_library_empty(self.books):
                return

            # Print table header
            print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'Year':<6} {'Status':<10}")
            print("-" * 75)

            # Print each book's details
            for book in self.books:
                print(f"{book.id:<5} {book.title:<30} {book.author:<20} {book.year:<6} {book.status:<10}")
        except Exception as e:
            logging.error(f"Unexpected error while displaying books: {e}")
            print("An unexpected error occurred while displaying the books.")

    def change_status(self) -> None:
        """
        Change the status of a book by ID.
        """
        try:
            if helper_functions.is_library_empty(self.books):
                return

            book_id = helper_functions.get_valid_id(self.books)
            book_to_update = next(book for book in self.books if book.id == book_id)
            new_status = helper_functions.get_valid_status()

            if book_to_update.status == new_status:
                print(f"The book is already '{new_status}'.")
                logging.info(f"Status update skipped for Book ID={book_id}. Already '{new_status}'.")
                return

            book_to_update.status = new_status
            self.save_books()
            print(f"Book ID {book_id} status updated to '{new_status}'.")
        except Exception as e:
            logging.error(f"Unexpected error while updating book status: {e}")
            print("An unexpected error occurred while updating the book status.")