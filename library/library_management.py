import json
import os
import logging
from library.models import Book
import library.helper_functions as helper_functions

class Library:
    def __init__(self, books_file: str = "books.json"):
        """
        Инициализировать экземпляр библиотеки.

        Аргументы:
            books_file (str): Путь к файлу, где хранятся данные о книгах.
        """
        self.books_file = books_file
        self.books = self.load_books()

    # --- Операции с файлами ---
    def load_books(self) -> list[Book]:
        """
        Загружает книги из JSON-файла.

        Возвращает:
            list[Book]: Список объектов Book.

        Исключения:
            JSONDecodeError: Если JSON-файл поврежден.
            IOError: Если произошла ошибка при чтении файла.
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
                return []
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
        Сохраняет книги в JSON-файл.

        Исключения:
            IOError: Если возникла проблема при записи в файл.
            Exception: Любая другая неожиданная ошибка при сохранении.
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

    # --- Основные операции ---
    def add_book(self) -> None:
        """
        Добавляет новую книгу в библиотеку.

        Исключения:
            Exception: Если произошла неожиданная ошибка при добавлении книги.
        """
        try:
            title = helper_functions.get_non_empty_string("Введите название книги: ")
            author = helper_functions.get_non_empty_string("Введите автора книги: ")
            year = helper_functions.get_valid_year()

            # Проверка на существование книги
            for book in self.books:
                if book.title.lower() == title.lower() and book.author.lower() == author.lower() and book.year == year:
                    print(f"Ошибка: Книга с таким названием, автором и годом уже существует в библиотеке.")
                    logging.warning(f"Duplicate book entry attempted: Title='{title}', Author='{author}', Year={year}")
                    return

            # Генерация уникального ID
            book_id = 1 if not self.books else max(book.id for book in self.books) + 1

            # Создание и добавление книги
            new_book = Book(book_id, title, author, year)
            self.books.append(new_book)
            self.save_books()
            print(f"Книга '{title}' успешно добавлена!")
        except Exception as e:
            logging.error(f"Unexpected error while adding a book: {e}")
            print("Произошла неожиданная ошибка при добавлении книги.")


    def delete_book(self) -> None:
        """
        Удаляет книгу из библиотеки по ID.

        Исключения:
            Exception: Если произошла неожиданная ошибка при удалении книги.
        """
        try:
            if helper_functions.is_library_empty(self.books):
                return

            book_id = helper_functions.get_valid_id(self.books)
            book_to_delete = next(book for book in self.books if book.id == book_id)
            self.books.remove(book_to_delete)
            self.save_books()
            print(f"Книга с ID {book_id} успешно удалена.")
        except Exception as e:
            logging.error(f"Unexpected error while deleting a book: {e}")
            print("Произошла неожиданная ошибка при удалении книги.")

    def search_books(self) -> None:
        """
        Ищет книги по названию, автору или году.

        Исключения:
            Exception: Если произошла неожиданная ошибка во время операции поиска.
        """
        try:
            if helper_functions.is_library_empty(self.books):
                return

            # Получить тип поиска
            search_type = helper_functions.get_search_choice()
            
            # Используйте get_non_empty_string для проверки корректности строки поиска
            search_query = helper_functions.get_non_empty_string(f"Введите {search_type}: ").lower()

            # Отфильтруйте книги по критериям поиска
            matching_books = helper_functions.filter_books(self.books, search_type, search_query)

            if matching_books:
                print(f"\nНайдено {len(matching_books)} книг(и):")
                
                # Вывод заголовка таблицы для результатов поиска
                print(f"{'ID':<5} {'Название':<30} {'Автор':<20} {'Год':<6} {'Статус':<10}")
                print("-" * 75)
                
                # Вывод данных о каждой найденной книге
                for book in matching_books:
                    print(f"{book.id:<5} {book.title:<30} {book.author:<20} {book.year:<6} {book.status:<10}")
            else:
                print("\nСовпадений не найдено.")
                logging.info(f"Search performed: Type='{search_type}', Query='{search_query}', Results=0")
        except Exception as e:
            logging.error(f"Unexpected error while searching for books: {e}")
            print("Произошла неожиданная ошибка при поиске книг.")

    def display_books(self) -> None:
        """
        Отображает все книги в библиотеке в табличном формате.

        Исключения:
            Exception: Если произошла неожиданная ошибка при отображении книг.
        """
        try:
            if helper_functions.is_library_empty(self.books):
                return

            # Вывод заголовка таблицы
            print(f"{'ID':<5} {'Название':<30} {'Автор':<20} {'Год':<6} {'Статус':<10}")
            print("-" * 75)

            # Вывод данных о каждой найденной книге
            for book in self.books:
                print(f"{book.id:<5} {book.title:<30} {book.author:<20} {book.year:<6} {book.status:<10}")
        except Exception as e:
            logging.error(f"Unexpected error while displaying books: {e}")
            print("Произошла неожиданная ошибка при отображении книг.")

    def change_status(self) -> None:
        """
        Изменяет статус книги по ID.

        Исключения:
            Exception: Если произошла неожиданная ошибка при обновлении статуса книги.
        """
        try:
            if helper_functions.is_library_empty(self.books):
                return

            book_id = helper_functions.get_valid_id(self.books)
            book_to_update = next(book for book in self.books if book.id == book_id)
            new_status = helper_functions.get_valid_status()

            if book_to_update.status == new_status:
                print(f"Книга уже имеет статус '{new_status}'.")
                logging.info(f"Status update skipped for Book ID={book_id}. Already '{new_status}'.")
                return

            book_to_update.status = new_status
            self.save_books()
            print(f"Статус книги с ID {book_id} обновлен на '{new_status}'.")
        except Exception as e:
            logging.error(f"Unexpected error while updating book status: {e}")
            print("Произошла неожиданная ошибка при обновлении статуса книги.")