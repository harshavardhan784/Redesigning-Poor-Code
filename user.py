from typing import List, Optional
from storage import UserStorage


class User:
    """
    Represents a user in the system.

    Attributes:
        name (str): The name of the user.
        user_id (str): A unique identifier for the user.
        borrowed_items (List[str]): A list of item IDs borrowed by the user.
    """

    def __init__(self, name: str, user_id: str):
        """
        Initialize a new User.

        Args:
            name (str): The name of the user.
            user_id (str): A unique identifier for the user.
        """
        self.name = name
        self.user_id = user_id
        self.borrowed_items: List[str] = []

    def borrow_item(self, item_id: str) -> None:
        """
        Add an item to the user's borrowed items list.

        Args:
            item_id (str): The ID of the item being borrowed.
        """
        if item_id not in self.borrowed_items:
            self.borrowed_items.append(item_id)

    def return_item(self, item_id: str) -> None:
        """
        Remove an item from the user's borrowed items list.

        Args:
            item_id (str): The ID of the item being returned.
        """
        if item_id in self.borrowed_items:
            self.borrowed_items.remove(item_id)

    def get_borrowed_items(self) -> List[str]:
        """
        Retrieve the list of borrowed item IDs.

        Returns:
            List[str]: A list of borrowed item IDs.
        """
        return self.borrowed_items

    def to_dict(self) -> dict:
        """
        Convert the User object to a dictionary for storage.

        Returns:
            dict: The dictionary representation of the User.
        """
        return {
            "name": self.name,
            "user_id": self.user_id,
            "borrowed_items": self.borrowed_items
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """
        Create a User object from a dictionary.

        Args:
            data (dict): A dictionary containing user information.

        Returns:
            User: The created User object.
        """
        user = cls(data["name"], data["user_id"])
        user.borrowed_items = data["borrowed_items"]
        return user

    def __str__(self) -> str:
        """
        Return a string representation of the User.

        Returns:
            str: A string representation of the User object.
        """
        return f"User(name='{self.name}', user_id='{self.user_id}', borrowed_items={self.borrowed_items})"


class UserManager:
    """
    Manages a collection of User objects, including adding, updating, and removing users.

    Attributes:
        storage (UserStorage): The storage handler for user data.
        users (List[User]): A list of User objects managed by the UserManager.
    """

    def __init__(self):
        """
        Initialize the UserManager and load existing users from storage.
        """
        self.storage = UserStorage()
        self.users = [User.from_dict(user) for user in self.storage.load_users()]

    def add_user(self, name: str, user_id: str) -> None:
        """
        Add a new user to the system.

        Args:
            name (str): The name of the new user.
            user_id (str): The unique identifier for the new user.

        Raises:
            ValueError: If a user with the same user_id already exists.
        """
        if self.get_user_by_id(user_id):
            raise ValueError(f"User with ID {user_id} already exists")
        user = User(name, user_id)
        self.users.append(user)
        self._save_users()

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Retrieve a user by their user_id.

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            Optional[User]: The User object if found, else None.
        """
        return next((user for user in self.users if user.user_id == user_id), None)

    def update_user(self, user_id: str, name: str = None) -> None:
        """
        Update a user's details.

        Args:
            user_id (str): The ID of the user to update.
            name (str, optional): The new name for the user. Defaults to None.

        Raises:
            ValueError: If the user with the given user_id is not found.
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        if name:
            user.name = name
        self._save_users()

    def delete_user(self, user_id: str) -> None:
        """
        Delete a user from the system.

        Args:
            user_id (str): The ID of the user to delete.

        Raises:
            ValueError: If the user with the given user_id is not found.
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        self.users.remove(user)
        self._save_users()

    def list_users(self) -> List[User]:
        """
        List all users in the system.

        Returns:
            List[User]: A list of all User objects.
        """
        return self.users

    def search_users(self, query: str) -> List[User]:
        """
        Search for users by name or user_id.

        Args:
            query (str): The search query string.

        Returns:
            List[User]: A list of User objects matching the search criteria.
        """
        query = query.lower()
        return [user for user in self.users if query in user.name.lower() or query in user.user_id.lower()]

    def _save_users(self):
        """
        Save the current list of users to storage.
        """
        self.storage.save_users([user.to_dict() for user in self.users])
