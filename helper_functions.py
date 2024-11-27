import logging
from datetime import datetime
from models import Book

def get_valid_id(books: list[Book]) -> int:
    """
    Prompt the user for a valid book ID that exists in the library.

    Args:
        books (list[Book]): List of books in the library.

    Returns:
        int: A valid book ID.
    """
    while True:
        try:
            book_id = int(input("Enter the ID of the book: "))
            if any(book.id == book_id for book in books):
                return book_id
            else:
                print(f"No book found with ID {book_id}. Please try again.")
                logging.warning(f"Invalid book ID entered: {book_id}")
        except ValueError:
            print("Invalid input. Please enter a numeric ID.")
            logging.warning("Non-numeric input entered for book ID.")

def get_valid_year() -> int:
    """
    Prompt the user for a valid year of publication.

    Returns:
        int: A valid year.
    """
    current_year = datetime.now().year
    while True:
        try:
            year = int(input("Enter year of publication: "))
            if 0 < year <= current_year:
                return year
            else:
                print(f"Invalid year. Please enter a year between 1 and {current_year}.")
                logging.warning(f"Invalid year entered: {year}")
        except ValueError:
            print("Invalid input. Please enter a numeric year.")
            logging.warning("Non-numeric input entered for year.")

def get_valid_status() -> str:
    """
    Prompt the user to select a valid book status.

    Returns:
        str: A valid status ("available" or "borrowed").
    """
    while True:
        print("\nStatus Options:")
        print("1. Available")
        print("2. Borrowed")
        status_choice = input("Enter your choice (1 or 2): ").strip()
        if status_choice == "1":
            return "available"
        elif status_choice == "2":
            return "borrowed"
        else:
            print("Invalid choice. Please enter 1 or 2.")
            logging.warning(f"Invalid status choice entered: {status_choice}")

def get_search_choice() -> str:
    """
    Prompt the user to select a valid search criterion.

    Returns:
        str: The search type ("title", "author", or "year").
    """
    while True:
        print("\nSearch Options:")
        print("1. Title")
        print("2. Author")
        print("3. Year")
        search_choice = input("Enter your choice (1-3): ").strip()
        if search_choice == "1":
            return "title"
        elif search_choice == "2":
            return "author"
        elif search_choice == "3":
            return "year"
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")
            logging.warning(f"Invalid search choice entered: {search_choice}")

def get_non_empty_string(prompt: str) -> str:
    """
    Prompt the user for a non-empty string.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        str: A non-empty string.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        else:
            print("Input cannot be empty. Please try again.")
            logging.warning("Empty input entered for a required field.")

def filter_books(books: list[Book], search_type: str, search_query: str) -> list[Book]:
    """
    Filter books based on the search type and query.

    Args:
        books (list[Book]): List of books to search.
        search_type (str): The field to search by ("title", "author", or "year").
        search_query (str): The search query string.

    Returns:
        list[Book]: List of books that match the search criteria.
    """
    filtered_books = [
        book for book in books
        if (search_type == "title" and search_query in book.title.lower()) or
           (search_type == "author" and search_query in book.author.lower()) or
           (search_type == "year" and search_query == str(book.year))
    ]
    if not filtered_books:
        logging.info(f"No books matched the search. Type='{search_type}', Query='{search_query}'")
    return filtered_books

def is_library_empty(books: list[Book]) -> bool:
    """
    Check if the library is empty and log a message if it is.

    Args:
        books (list[Book]): List of books in the library.

    Returns:
        bool: True if the library is empty, False otherwise.
    """
    if not books:
        print("No books in the library.")
        logging.info("Operation attempted, but the library is empty.")
        return True
    return False