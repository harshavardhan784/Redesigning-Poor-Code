# Library Management System

This project is a Library Management System that allows users to manage books, users, and checkout operations. It supports features like borrowing and returning books, tracking overdue items, and managing user and book information.

## Features

- **User Management**: Manage user records, including borrowing history.
- **Book Management**: Track availability and details of books.
- **Checkout Management**: Handle book borrowing and returning, with due dates and overdue checks.
- **Persistent Storage**: Save and load data for users, books, and checkouts.

## Project Structure

- `book.py`: Contains the `Book` and `BookManager` classes for managing book-related operations.
- `user.py`: Contains the `User` and `UserManager` classes for managing user-related operations.
- `checkout.py`: Contains the `Checkout` and `CheckoutManager` classes for handling borrowing and returning items.
- `storage.py`: Provides persistent storage mechanisms for books, users, and checkouts.

## Usage

1. **Add Users and Books**: Use the `UserManager` and `BookManager` to add users and books to the system.
2. **Checkout Books**: Users can borrow books using the `CheckoutManager`. Books will be marked as unavailable.
3. **Return Books**: Once a book is returned, it will be available for others to borrow.
4. **Check for Overdue Books**: The system can list books that are overdue for return.

## Example

Here’s an example of how to use the system:

```python
from book import BookManager
from user import UserManager
from checkout import CheckoutManager

# Initialize managers
book_manager = BookManager()
user_manager = UserManager()
checkout_manager = CheckoutManager(book_manager, user_manager)

# Add a book and a user
book_manager.add_book("1234567890", "The Great Gatsby", "F. Scott Fitzgerald")
user_manager.add_user("1", "John Doe")

# Checkout a book
checkout_manager.checkout_book("1", "1234567890")

# List all checkouts
for checkout in checkout_manager.list_checkouts():
    print(checkout)

# Return the book
checkout_manager.return_book("1", "1234567890")
