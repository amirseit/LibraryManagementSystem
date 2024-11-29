import logging
from datetime import datetime
from library.models import Book

def get_valid_id(books: list[Book]) -> int:
    """
    Запрашивает у пользователя действительный ID книги, который существует в библиотеке.

    Аргументы:
        books (list[Book]): Список книг в библиотеке.

    Возвращает:
        int: Действительный ID книги.

    Исключения:
        ValueError: Если пользователь вводит нечисловое значение.
    """
    while True:
        try:
            book_id = int(input("Введите ID книги: "))
            if any(book.id == book_id for book in books):
                return book_id
            else:
                print(f"Книга с ID {book_id} не найдена. Пожалуйста, попробуйте снова.")
                logging.warning(f"Invalid book ID entered: {book_id}")
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите числовой ID.")
            logging.warning("Non-numeric input entered for book ID.")

def get_valid_year() -> int:
    """
    Запрашивает у пользователя действительный год публикации.

    Возвращает:
        int: Действительный год.

    Исключения:
        ValueError: Если пользователь вводит нечисловое значение.
    """
    current_year = datetime.now().year
    while True:
        try:
            year = int(input("Введите год публикации: "))
            if 0 < year <= current_year:
                return year
            else:
                print(f"Недействительный год. Пожалуйста, введите год в диапазоне от 1 до {current_year}.")
                logging.warning(f"Invalid year entered: {year}")
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите числовой год.")
            logging.warning("Non-numeric input entered for year.")

def get_valid_status() -> str:
    """
    Запрашивает у пользователя выбор действительного статуса книги.

    Возвращает:
        str: Действительный статус ("available" или "borrowed").
    """
    while True:
        print("\nОпции статуса:")
        print("1. Available")
        print("2. Borrowed")
        status_choice = input("Введите ваш выбор (1 или 2): ").strip()
        if status_choice == "1":
            return "available"
        elif status_choice == "2":
            return "borrowed"
        else:
            print("Неверный выбор. Пожалуйста, введите 1 или 2.")
            logging.warning(f"Invalid status choice entered: {status_choice}")

def get_search_choice() -> str:
    """
    Запрашивает у пользователя выбор действительного критерия поиска.

    Возвращает:
        str: Тип поиска ("title", "author" или "year").
    """
    while True:
        print("\nОпции поиска:")
        print("1. Title")
        print("2. Author")
        print("3. Year")
        search_choice = input("Введите ваш выбор (1-3): ").strip()
        if search_choice == "1":
            return "title"
        elif search_choice == "2":
            return "author"
        elif search_choice == "3":
            return "year"
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 3.")
            logging.warning(f"Invalid search choice entered: {search_choice}")

def get_non_empty_string(prompt: str) -> str:
    """
    Запрашивает у пользователя непустой string.

    Аргументы:
        prompt (str): Сообщение для отображения пользователю.

    Возвращает:
        str: Непустой string.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        else:
            print("Ввод не может быть пустым. Пожалуйста, попробуйте снова.")
            logging.warning("Empty input entered for a required field.")

def filter_books(books: list[Book], search_type: str, search_query: str) -> list[Book]:
    """
    Фильтровать книги на основе типа поиска и запроса.

    Аргументы:
        books (list[Book]): Список книг для поиска.
        search_type (str): Поле для поиска ("title", "author" или "year").
        search_query (str): Строка поиска.

    Возвращает:
        list[Book]: Список книг, соответствующих критериям поиска.
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
     Проверьте, пуста ли библиотека, и выведите сообщение, если это так.

    Аргументы:
        books (list[Book]): Список книг в библиотеке.

    Возвращает:
        bool: True, если библиотека пуста, иначе False.
    """
    if not books:
        print("В библиотеке нет книг.")
        logging.info("Operation attempted, but the library is empty.")
        return True
    return False