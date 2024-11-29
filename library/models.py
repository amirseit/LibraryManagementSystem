class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "available"):
        """
        Инициализирует экземпляр класса Book.
        
        Аргументы:
            book_id (int): Уникальный идентификатор книги.
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания.
            status (str): Статус книги ("available" или "borrowed"). По умолчанию "available".
        """
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> dict:
        """
        Преобразует экземпляр Book в словарь.

        Возвращает:
            dict: Представление экземпляра Book в виде словаря.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: dict) -> 'Book':
        """
        Создает экземпляр Book из словаря.

        Аргументы:
            data (dict): Словарь, содержащий данные о книге.

        Возвращает:
            Book: Экземпляр Book, созданный из словаря.
        """
        return Book(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data["status"]
        )

# Пример использования
if __name__ == "__main__":
    # Создание новой книги
    book = Book(1, "1984", "George Orwell", 1949)
    print("Book as a dictionary:", book.to_dict())

    # Сериализация и десериализация с использованием словарей
    book_data = book.to_dict()
    recreated_book = Book.from_dict(book_data)
    print("Recreated Book:", recreated_book.to_dict())
