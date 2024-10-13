from datetime import datetime, timedelta
from book import BookManager
from user import UserManager
from typing import List, Optional
from storage import BookStorage, UserStorage, CheckoutStorage

class Checkout:
    """
    Represents a checkout transaction for a library system.

    Attributes:
        user_id (str): The ID of the user who borrowed the item.
        item_id (str): The ID of the borrowed item (e.g., book ISBN).
        checkout_date (datetime): The date when the item was checked out.
        due_date (datetime): The date by which the item should be returned.
        return_date (Optional[datetime]): The date when the item was returned, if returned.
    """

    def __init__(self, user_id: str, item_id: str, checkout_date: datetime = None, due_date: datetime = None):
        """
        Initialize a Checkout object.

        Args:
            user_id (str): The ID of the user who is checking out the item.
            item_id (str): The ID of the item being checked out (e.g., book ISBN).
            checkout_date (Optional[datetime]): The date of the checkout. Defaults to the current date.
            due_date (Optional[datetime]): The due date for the item. Defaults to 14 days from the checkout date.
        """
        self.user_id = user_id
        self.item_id = item_id
        self.checkout_date = checkout_date or datetime.now()
        self.due_date = due_date or (self.checkout_date + timedelta(days=14))  # Default loan period of 14 days
        self.return_date: Optional[datetime] = None

    def return_item(self) -> None:
        """
        Mark the item as returned by setting the return date to the current date.
        """
        self.return_date = datetime.now()

    def to_dict(self) -> dict:
        """
        Convert the Checkout object to a dictionary for storage.

        Returns:
            dict: A dictionary representation of the Checkout object.
        """
        return {
            "user_id": self.user_id,
            "item_id": self.item_id,
            "checkout_date": self.checkout_date.isoformat(),
            "due_date": self.due_date.isoformat(),
            "return_date": self.return_date.isoformat() if self.return_date else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Checkout':
        """
        Create a Checkout object from a dictionary.

        Args:
            data (dict): A dictionary containing checkout data.

        Returns:
            Checkout: A Checkout object created from the given dictionary.
        """
        checkout = cls(
            data["user_id"],
            data["item_id"],
            datetime.fromisoformat(data["checkout_date"]),
            datetime.fromisoformat(data["due_date"])
        )
        if data["return_date"]:
            checkout.return_date = datetime.fromisoformat(data["return_date"])
        return checkout

    def __str__(self) -> str:
        """
        Generate a string representation of the Checkout object.

        Returns:
            str: A string representation indicating the checkout status.
        """
        status = "Returned" if self.return_date else "Checked Out"
        return f"Checkout(user_id='{self.user_id}', item_id='{self.item_id}', status='{status}')"


class CheckoutManager:
    """
    Manages a collection of checkout transactions in the library system.

    Attributes:
        book_manager (BookManager): An instance of the BookManager to manage book-related operations.
        user_manager (UserManager): An instance of the UserManager to manage user-related operations.
        checkouts (List[Checkout]): A list of all current checkouts in the system.
    """

    def __init__(self, book_manager: BookManager, user_manager: UserManager):
        """
        Initialize a CheckoutManager.

        Args:
            book_manager (BookManager): The manager responsible for book operations.
            user_manager (UserManager): The manager responsible for user operations.
        """
        self.storage = CheckoutStorage()
        self.checkouts = [Checkout.from_dict(checkout) for checkout in self.storage.load_checkouts()]
        self.book_manager = book_manager
        self.user_manager = user_manager

    def checkout_book(self, user_id: str, isbn: str) -> None:
        """
        Checkout a book to a user.

        Args:
            user_id (str): The ID of the user checking out the book.
            isbn (str): The ISBN of the book being checked out.

        Raises:
            ValueError: If the user or book is not found, or if the book is not available.
        """
        user = self.user_manager.get_user_by_id(user_id)
        book = self.book_manager.get_book_by_isbn(isbn)

        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        if not book:
            raise ValueError(f"Book with ISBN {isbn} not found")
        if not book.is_available:
            raise ValueError(f"Book with ISBN {isbn} is not available")

        checkout = Checkout(user_id, isbn)
        self.checkouts.append(checkout)
        book.is_available = False
        user.borrow_item(isbn)

        self._save_checkouts()
        self.book_manager._save_books()
        self.user_manager._save_users()

    def return_book(self, user_id: str, isbn: str) -> None:
        """
        Return a book that was checked out by a user.

        Args:
            user_id (str): The ID of the user returning the book.
            isbn (str): The ISBN of the book being returned.

        Raises:
            ValueError: If the user, book, or active checkout is not found.
        """
        user = self.user_manager.get_user_by_id(user_id)
        book = self.book_manager.get_book_by_isbn(isbn)

        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        if not book:
            raise ValueError(f"Book with ISBN {isbn} not found")

        checkout = next((c for c in self.checkouts if c.user_id == user_id and c.item_id == isbn and not c.return_date), None)
        if not checkout:
            raise ValueError(f"No active checkout found for user {user_id} and book {isbn}")

        checkout.return_item()
        book.is_available = True
        user.return_item(isbn)

        self._save_checkouts()
        self.book_manager._save_books()
        self.user_manager._save_users()

    def list_checkouts(self) -> List[Checkout]:
        """
        List all checkout transactions.

        Returns:
            List[Checkout]: A list of all checkout transactions.
        """
        return self.checkouts

    def _save_checkouts(self):
        """
        Save the current list of checkouts to persistent storage.
        """
        self.storage.save_checkouts([checkout.to_dict() for checkout in self.checkouts])
