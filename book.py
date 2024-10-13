from abc import ABC, abstractmethod
from typing import List, Optional
from storage import BookStorage

class LibraryItem(ABC):
    """
    Abstract base class representing a library item.

    Attributes:
        title (str): The title of the item.
        item_id (str): The unique identifier for the item (e.g., ISBN for books).
        is_available (bool): Availability status of the item.
    """
    
    def __init__(self, title: str, item_id: str):
        """
        Initialize a new library item.

        Args:
            title (str): The title of the item.
            item_id (str): The unique identifier for the item.
        """
        self.title = title
        self.item_id = item_id
        self.is_available = True

    @abstractmethod
    def to_dict(self):
        """
        Convert the LibraryItem object to a dictionary representation for storage.
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        """
        Create a LibraryItem object from a dictionary representation.

        Args:
            data (dict): A dictionary containing item information.
        """
        pass


class Book(LibraryItem):
    """
    Represents a book in the library system.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        isbn (str): The ISBN number of the book (used as item_id).
    """

    def __init__(self, title: str, author: str, isbn: str):
        """
        Initialize a new Book.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            isbn (str): The ISBN number of the book.
        """
        super().__init__(title, isbn)
        self.author = author

    def to_dict(self) -> dict:
        """
        Convert the Book object to a dictionary representation for storage.

        Returns:
            dict: A dictionary containing the book's data.
        """
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.item_id,
            "is_available": self.is_available
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """
        Create a Book object from a dictionary representation.

        Args:
            data (dict): A dictionary containing the book's data.

        Returns:
            Book: The created Book object.
        """
        book = cls(data["title"], data["author"], data["isbn"])
        book.is_available = data["is_available"]
        return book

    def __str__(self) -> str:
        """
        Return a string representation of the Book object.

        Returns:
            str: A string describing the book.
        """
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.item_id}', available={self.is_available})"


class BookManager:
    """
    Manages the library's book inventory, including adding, updating, and deleting books.

    Attributes:
        storage (BookStorage): The storage handler for book data.
        books (List[Book]): List of books managed by the BookManager.
    """

    def __init__(self):
        """
        Initialize the BookManager with existing books loaded from storage.
        """
        self.storage = BookStorage()
        self.books = [Book.from_dict(book) for book in self.storage.load_books()]

    def add_book(self, title: str, author: str, isbn: str) -> None:
        """
        Add a new book to the inventory.

        Args:
            title (str): The title of the book.
            author (str): The author of the book.
            isbn (str): The ISBN of the book.

        Raises:
            ValueError: If a book with the same ISBN already exists.
        """
        if self.get_book_by_isbn(isbn):
            raise ValueError(f"Book with ISBN {isbn} already exists")
        book = Book(title, author, isbn)
        self.books.append(book)
        self._save_books()

    def get_book_by_isbn(self, isbn: str) -> Optional[Book]:
        """
        Retrieve a book by its ISBN.

        Args:
            isbn (str): The ISBN of the book to retrieve.

        Returns:
            Optional[Book]: The book if found, None otherwise.
        """
        return next((book for book in self.books if book.item_id == isbn), None)

    def update_book(self, isbn: str, title: str = None, author: str = None) -> None:
        """
        Update the details of an existing book.

        Args:
            isbn (str): The ISBN of the book to update.
            title (Optional[str]): The new title of the book, if updating.
            author (Optional[str]): The new author of the book, if updating.

        Raises:
            ValueError: If the book with the given ISBN is not found.
        """
        book = self.get_book_by_isbn(isbn)
        if not book:
            raise ValueError(f"Book with ISBN {isbn} not found")
        if title:
            book.title = title
        if author:
            book.author = author
        self._save_books()

    def delete_book(self, isbn: str) -> None:
        """
        Delete a book from the inventory.

        Args:
            isbn (str): The ISBN of the book to delete.

        Raises:
            ValueError: If the book with the given ISBN is not found.
        """
        book = self.get_book_by_isbn(isbn)
        if not book:
            raise ValueError(f"Book with ISBN {isbn} not found")
        self.books.remove(book)
        self._save_books()

    def list_books(self) -> List[Book]:
        """
        List all books in the library.

        Returns:
            List[Book]: A list of all Book objects in the library.
        """
        return self.books

    def search_books(self, query: str) -> List[Book]:
        """
        Search for books by title, author, or ISBN.

        Args:
            query (str): The search query.

        Returns:
            List[Book]: A list of books that match the search criteria.
        """
        query = query.lower()
        return [book for book in self.books if query in book.title.lower() or query in book.author.lower() or query in book.item_id.lower()]

    def _save_books(self):
        """
        Save the current list of books to storage.
        """
        self.storage.save_books([book.to_dict() for book in self.books])
