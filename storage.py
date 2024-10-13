import json
from typing import List, Dict, Any
import os

class Storage:
    """
    A base class for handling the storage of data to and from a JSON file.

    Attributes:
        file_path (str): The path to the JSON file used for storage.
    """

    def __init__(self, file_path: str):
        """
        Initialize the Storage class with a file path.

        Args:
            file_path (str): The file path where data will be saved and loaded.
        """
        self.file_path = file_path

        def save_data(self, data: Dict[str, List[Dict[str, Any]]]):
        """
        Save data to the JSON file.

        Args:
            data (Dict[str, List[Dict[str, Any]]]): The data to save in the format
            of a dictionary containing lists of dictionaries.
        """
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=2, default=str)

    def load_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Load data from the JSON file.

        Returns:
            Dict[str, List[Dict[str, Any]]]: The loaded data in the form of a dictionary.
            Returns default empty lists for "books", "users", and "checkouts" if the file does not exist.
        """
        if not os.path.exists(self.file_path):
            # If the file doesn't exist, return an empty data structure
            return {"books": [], "users": [], "checkouts": []}
        with open(self.file_path, 'r') as file:
            # Load and return the data from the JSON file
            return json.load(file)

class BookStorage(Storage):
    """
    A storage handler for book-related data, extending the Storage class.
    Manages the saving and loading of book data to 'books.json'.
    """

    def __init__(self):
        """
        Initialize the BookStorage with the 'books.json' file.
        """
        super().__init__('books.json')

    def save_books(self, books: List[Dict[str, Any]]):
        """
        Save the list of books to the JSON file.

        Args:
            books (List[Dict[str, Any]]): A list of dictionaries containing book information.
        """
        self.save_data({"books": books})

    def load_books(self) -> List[Dict[str, Any]]:
        """
        Load the list of books from the JSON file.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing book information.
        """
        return self.load_data().get("books", [])

class UserStorage(Storage):
    """
    A storage handler for user-related data, extending the Storage class.
    Manages the saving and loading of user data to 'users.json'.
    """

    def __init__(self):
        """
        Initialize the UserStorage with the 'users.json' file.
        """
        super().__init__('users.json')

    def save_users(self, users: List[Dict[str, Any]]):
        """
        Save the list of users to the JSON file.

        Args:
            users (List[Dict[str, Any]]): A list of dictionaries containing user information.
        """
        self.save_data({"users": users})

    def load_users(self) -> List[Dict[str, Any]]:
        """
        Load the list of users from the JSON file.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing user information.
        """
        return self.load_data().get("users", [])

class CheckoutStorage(Storage):
    """
    A storage handler for checkout-related data, extending the Storage class.
    Manages the saving and loading of checkout data to 'checkouts.json'.
    """

    def __init__(self):
        """
        Initialize the CheckoutStorage with the 'checkouts.json' file.
        """
        super().__init__('checkouts.json')

    def save_checkouts(self, checkouts: List[Dict[str, Any]]):
        """
        Save the list of checkouts to the JSON file.

        Args:
            checkouts (List[Dict[str, Any]]): A list of dictionaries containing checkout information.
        """
        self.save_data({"checkouts": checkouts})

    def load_checkouts(self) -> List[Dict[str, Any]]:
        """
        Load the list of checkouts from the JSON file.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing checkout information.
        """
        return self.load_data().get("checkouts", [])
