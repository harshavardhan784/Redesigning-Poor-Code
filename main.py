import logging
from book import BookManager
from user import UserManager
from check import CheckoutManager

# Configure logging for the Library Management System
logging.basicConfig(
    filename='library.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LibraryManagementSystem:
    """
    Main class for the Library Management System.
    
    This class integrates BookManager, UserManager, and CheckoutManager
    to provide a complete library management solution. It allows for
    managing books and users, as well as checking out and returning books.
    """

    def __init__(self):
        """
        Initialize the Library Management System with its component managers.
        
        The component managers include:
        - BookManager: Handles book-related operations.
        - UserManager: Manages user-related functionalities.
        - CheckoutManager: Coordinates the process of checking out and returning books.
        """
        self.book_manager = BookManager()
        self.user_manager = UserManager()
        self.checkout_manager = CheckoutManager(self.book_manager, self.user_manager)
    
    def run(self):
        """
        Run the main loop of the Library Management System.
        
        Continuously displays the main menu and processes the user's menu choice
        until the user chooses to exit.
        """
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            self.process_choice(choice)
            
    def display_menu(self):
        """
        Display the main menu options for the Library Management System.
        
        The menu options include adding, listing, updating, and deleting books and users,
        as well as checking out and returning books.
        """
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. List Books")
        print("3. Update Book")
        print("4. Delete Book")
        print("5. Search Books")
        print("6. Add User")
        print("7. Update User")
        print("8. List Users")
        print("9. Search Users")
        print("10. Delete User")
        print("11. Checkout Book")
        print("12. Return Book")
        print("13. Exit")
        
    def process_choice(self, choice):
        """
        Process the user's menu choice.
        
        Args:
            choice (str): The user's menu selection as a string.
            
        Depending on the choice, it calls the corresponding method to perform 
        the desired operation (e.g., add a book, list users, checkout a book).
        """
        try:
            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.list_books()
            elif choice == '3':
                self.update_book()
            elif choice == '4':
                self.delete_book()
            elif choice == '5':
                self.search_books()
            elif choice == '6':
                self.add_user()
            elif choice == '7':
                self.update_user()
            elif choice == '8':
                self.list_users()
            elif choice == '9':
                self.search_users()
            elif choice == '10':
                self.delete_user()
            elif choice == '11':
                self.checkout_book()
            elif choice == '12':
                self.return_book()
            elif choice == '13':
                print("Thank you for using the Library Management System. Goodbye!")
                exit()
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            # Log any errors that occur during menu processing
            print(f"An error occurred: {str(e)}")
            logging.error(f"Error in process_choice: {str(e)}")
                       
    def add_book(self):
        """
        Add a new book to the library.
        
        Prompts the user to input the book's title, author, and ISBN, then adds the book
        using the BookManager.
        """
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        isbn = input("Enter book ISBN: ")
        self.book_manager.add_book(title, author, isbn)
        print("Book added successfully.")
        logging.info(f"Book added: {isbn}")
    
    def update_book(self):
        """
        Update an existing book's information.
        
        Prompts the user for the book's ISBN and the new title and/or author, then updates
        the book using the BookManager.
        """
        isbn = input("Enter ISBN of the book to update: ")
        title = input("Enter new title (press Enter to skip): ")
        author = input("Enter new author (press Enter to skip): ")
        self.book_manager.update_book(isbn, title or None, author or None)
        print("Book updated successfully.")
        logging.info(f"Book updated: {isbn}")
        
    def delete_book(self):
        """
        Delete a book from the library.
        
        Prompts the user to input the book's ISBN, then deletes the book using the BookManager.
        """
        isbn = input("Enter ISBN of the book to delete: ")
        self.book_manager.delete_book(isbn)
        print("Book deleted successfully.")
        logging.info(f"Book deleted: {isbn}")

    def list_books(self):
        """
        List all books in the library.
        
        Retrieves a list of all books from the BookManager and displays them.
        """
        books = self.book_manager.list_books()
        for book in books:
            print(book)

    def search_books(self):
        """
        Search for books based on a query.
        
        Prompts the user for a search query, then searches for matching books
        using the BookManager.
        """
        query = input("Enter search query: ")
        books = self.book_manager.search_books(query)
        for book in books:
            print(book)

    def add_user(self):
        """
        Add a new user to the library system.
        
        Prompts the user to input the user's name and ID, then adds the user
        using the UserManager.
        """
        name = input("Enter user name: ")
        user_id = input("Enter user ID: ")
        self.user_manager.add_user(name, user_id)
        print("User added successfully.")
        logging.info(f"User added: {user_id}")

    def update_user(self):
        """
        Update an existing user's information.
        
        Prompts the user for the user's ID and the new name, then updates the user
        using the UserManager.
        """
        user_id = input("Enter ID of the user to update: ")
        name = input("Enter new name: ")
        self.user_manager.update_user(user_id, name)
        print("User updated successfully.")
        logging.info(f"User updated: {user_id}")

    def delete_user(self):
        """
        Delete a user from the library system.
        
        Prompts the user for the user's ID, then deletes the user using the UserManager.
        """
        user_id = input("Enter ID of the user to delete: ")
        self.user_manager.delete_user(user_id)
        print("User deleted successfully.")
        logging.info(f"User deleted: {user_id}")

    def list_users(self):
        """
        List all users in the library system.
        
        Retrieves a list of all users from the UserManager and displays them.
        """
        users = self.user_manager.list_users()
        for user in users:
            print(user)

    def search_users(self):
        """
        Search for users based on a query.
        
        Prompts the user for a search query, then searches for matching users
        using the UserManager.
        """
        query = input("Enter search query: ")
        users = self.user_manager.search_users(query)
        for user in users:
            print(user)

    def checkout_book(self):
        """
        Check out a book to a user.
        
        Prompts the user to input their ID and the book's ISBN, then checks out the book
        using the CheckoutManager.
        """
        user_id = input("Enter user ID: ")
        isbn = input("Enter book ISBN: ")
        self.checkout_manager.checkout_book(user_id, isbn)
        print("Book checked out successfully.")
        logging.info(f"Book checked out: {isbn} by user: {user_id}")

    def return_book(self):
        """
        Return a book from a user.
        
        Prompts the user for their ID and the book's ISBN, then returns the book
        using the CheckoutManager.
        """
        user_id = input("Enter user ID: ")
        isbn = input("Enter book ISBN: ")
        self.checkout_manager.return_book(user_id, isbn)
        print("Book returned successfully.")
        logging.info(f"Book returned: {isbn} by user: {user_id}")
    
def main():
    """
    Main function to run the Library Management System.
    
    Creates an instance of LibraryManagementSystem and starts the main loop.
    """
    library_system = LibraryManagementSystem()
    library_system.run()

if __name__ == "__main__":
    main()
