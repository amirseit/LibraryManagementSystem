class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "available"):
        """
        Initializes a Book instance.
        
        Args:
            book_id (int): Unique identifier for the book.
            title (str): Title of the book.
            author (str): Author of the book.
            year (int): Year of publication.
            status (str): Status of the book ("available" or "borrowed"). Default is "available".
        """
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> dict:
        """
        Converts the Book instance into a dictionary.

        Returns:
            dict: A dictionary representation of the Book instance.
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
        Creates a Book instance from a dictionary.

        Args:
            data (dict): A dictionary containing book data.

        Returns:
            Book: A Book instance created from the dictionary.
        """
        return Book(
            book_id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data["status"]
        )

# Example Usage
if __name__ == "__main__":
    # Create a new book
    book = Book(1, "1984", "George Orwell", 1949)
    print("Book as a dictionary:", book.to_dict())

    # Serialize and deserialize using dictionaries
    book_data = book.to_dict()
    recreated_book = Book.from_dict(book_data)
    print("Recreated Book:", recreated_book.to_dict())
