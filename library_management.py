import json
import os
import logging
from models import Book
import helper_functions

# File path for storing book data
BOOKS_FILE = "books.json"

# --- File Operations ---

def load_books() -> list[Book]:
    """
    Load books from the JSON file.

    Returns:
        list[Book]: A list of Book objects. If the file is missing or corrupted, return an empty list.
    """
    if os.path.exists(BOOKS_FILE):
        try:
            with open(BOOKS_FILE, "r") as file:
                books_data = json.load(file)
                return [Book.from_dict(book) for book in books_data]
        except json.JSONDecodeError:
            error_message = "Error: books.json is corrupted. Starting with an empty library."
            print(error_message)
            logging.error(error_message)
            return []  # Return an empty list if the file is corrupted
        except Exception as e:
            error_message = f"Unexpected error while loading books: {e}"
            print(error_message)
            logging.error(error_message)
            return []  # Return an empty list for any other unexpected errors
    else:
        warning_message = "Warning: books.json file not found. A new file will be created."
        print(warning_message)
        logging.warning(warning_message)
        return []  # Return an empty list if the file does not exist

def save_books(books: list[Book]) -> None:
    """
    Save books to the JSON file.

    Args:
        books (list[Book]): A list of Book objects.

    Raises:
        IOError: If there is an issue writing to the file.
    """
    try:
        with open(BOOKS_FILE, "w") as file:
            json.dump([book.to_dict() for book in books], file, indent=4)
    except IOError as e:
        error_message = f"Error: Unable to save books to {BOOKS_FILE}. {e}"
        print(error_message)
        logging.error(error_message)
    except Exception as e:
        error_message = f"Unexpected error while saving books: {e}"
        print(error_message)
        logging.error(error_message)

# --- Core Operations ---

def add_book():
    """
    Add a new book to the library.
    """
    try:
        books = load_books()
        title = helper_functions.get_non_empty_string("Enter book title: ")
        author = helper_functions.get_non_empty_string("Enter book author: ")
        year = helper_functions.get_valid_year()

        # Generate a unique ID
        book_id = 1 if not books else max(book.id for book in books) + 1

        # Create and add the book
        new_book = Book(book_id, title, author, year)
        books.append(new_book)
        save_books(books)
        print(f"Book '{title}' added successfully!")
    except Exception as e:
        logging.error(f"Unexpected error while adding a book: {e}")
        print("An unexpected error occurred while adding the book.")

def delete_book():
    """
    Delete a book from the library by ID.
    """
    try:
        books = load_books()
        if helper_functions.is_library_empty(books):
            return
        
        book_id = helper_functions.get_valid_id(books)
        book_to_delete = next(book for book in books if book.id == book_id)
        books.remove(book_to_delete)
        save_books(books)
        print(f"Book ID {book_id} deleted successfully.")
    except Exception as e:
        logging.error(f"Unexpected error while deleting a book: {e}")
        print("An unexpected error occurred while deleting the book.")

def search_books():
    """
    Search for books by title, author, or year.
    """
    try:
        books = load_books()
        if helper_functions.is_library_empty(books):
            return
        
        search_type = helper_functions.get_search_choice()
        search_query = input(f"Enter {search_type}: ").strip().lower()

        matching_books = helper_functions.filter_books(books, search_type, search_query)

        if matching_books:
            print(f"\nFound {len(matching_books)} book(s):")
            for book in matching_books:
                print(book.to_dict())
        else:
            print("\nNo matching books found.")
            logging.info(f"Search performed: Type='{search_type}', Query='{search_query}', Results=0")
    except Exception as e:
        logging.error(f"Unexpected error while searching for books: {e}")
        print("An unexpected error occurred while searching for books.")

def display_books():
    """
    Display all books in the library in a tabular format.
    """
    try:
        books = load_books()
        if helper_functions.is_library_empty(books):
            return
        
        # Print table header
        print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'Year':<6} {'Status':<10}")
        print("-" * 75)

        # Print each book's details
        for book in books:
            print(f"{book.id:<5} {book.title:<30} {book.author:<20} {book.year:<6} {book.status:<10}")
    except Exception as e:
        logging.error(f"Unexpected error while displaying books: {e}")
        print("An unexpected error occurred while displaying the books.")

def change_status():
    """
    Change the status of a book by ID.
    """
    try:
        books = load_books()
        if helper_functions.is_library_empty(books):
            return
        
        book_id = helper_functions.get_valid_id(books)
        book_to_update = next(book for book in books if book.id == book_id)
        new_status = helper_functions.get_valid_status()

        if book_to_update.status == new_status:
            print(f"The book is already '{new_status}'.")
            logging.info(f"Status update skipped for Book ID={book_id}. Already '{new_status}'.")
            return

        book_to_update.status = new_status
        save_books(books)
        print(f"Book ID {book_id} status updated to '{new_status}'.")
    except Exception as e:
        logging.error(f"Unexpected error while updating book status: {e}")
        print("An unexpected error occurred while updating the book status.")