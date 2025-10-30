import datetime
import os

class LMS:
    """
    This class is used to keep records of books in the library.
    It has four main modules: display books, issue books, return books, and add books.
    """
    def __init__(self, list_of_books, library_name):
        # Initialize basic attributes
        self.list_of_books = list_of_books  # File path to the book list
        self.library_name = library_name
        self.books_dictionary = {}
        self.bookid = 101 # Starting book ID

        # Read the initial list of books from the text file and populate the dictionary
        try:
            # Use 'r' for reading
            with open(self.list_of_books, 'r') as bk:
                content = bk.readlines()
            
            for line in content:
                # Remove newline characters and clean up the title
                book_title = line.replace('\n', '').strip() 
                
                # Populate the dictionary
                self.books_dictionary.update({
                    str(self.bookid): {
                        'books title': book_title,
                        'lender name': '',
                        'issue date': '',
                        'status': 'available'
                    }
                })
                self.bookid += 1 # Increment book ID for the next book in the file

        except FileNotFoundError:
            print(f"Error: The file '{list_of_books}' was not found.")
        except Exception as e:
            print(f"An unexpected error occurred during initialization: {e}")


    def display_books(self):
        print("\n" + "="*50)
        print(f"{' '*10}--- List of Books in {self.library_name} ---")
        print("="*50)
        print(f"{'ID':<10}{'Title':<40}{'Status':<15}")
        print("-" * 65)

        for key, value in self.books_dictionary.items():
            # key is the Book ID
            title = value.get('books title', 'N/A')
            status = value.get('status', 'N/A')
            print(f"{key:<10}{title:<40}{status:<15}")
        print("=" * 50)


    def issue_books(self):
        books_id = input("Enter Book ID to issue: ").strip()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if books_id in self.books_dictionary.keys():
            book_info = self.books_dictionary[books_id]
            
            if book_info['status'] == 'available':
                user_name = input("Enter your name: ").strip()
                if not user_name:
                    print("Lender name cannot be blank.")
                    return self.issue_books()

                # Update status
                book_info['lender name'] = user_name
                book_info['issue date'] = current_date
                book_info['status'] = 'already issued'
                print(f"\nBook '{book_info['books title']}' (ID: {books_id}) successfully issued to {user_name}.")
                
            else:
                # Book is already issued
                print("-" * 50)
                print(f"This book (ID: {books_id}) is already issued to {book_info['lender name']}.")
                print(f"Issue Date: {book_info['issue date']}")
                print("-" * 50)
        else:
            print("Error: Book ID not found in the database.")
            # return self.issue_books() # Removed to prevent infinite recursion on error


    def add_books(self):
        new_book_title = input("Enter new book title to add: ").strip()

        if not new_book_title:
            print("Book title cannot be blank.")
            return self.add_books()
        elif len(new_book_title) > 50: # Increased from 25 for practicality
            print("Book title length is too long (Max 50 characters).")
            return self.add_books()
        else:
            # 1. Append the new title to the text file (our persistent database)
            # Use 'a' for appending
            with open(self.list_of_books, 'a') as bk:
                bk.write(f"\n{new_book_title}")
            
            # 2. Update the in-memory dictionary
            # Find the next available ID by converting all keys to integers and finding the max
            try:
                max_id = int(max(self.books_dictionary.keys()))
            except ValueError:
                # Handles case where dictionary is empty or keys are not convertible
                max_id = 100 

            next_id = str(max_id + 1)

            self.books_dictionary.update({
                next_id: {
                    'books title': new_book_title,
                    'lender name': '',
                    'issue date': '',
                    'status': 'available'
                }
            })
            
            print(f"\nBook '{new_book_title}' (ID: {next_id}) has been added successfully.")


    def return_book(self):
        books_id = input("Enter Book ID to return: ").strip()

        if books_id in self.books_dictionary.keys():
            book_info = self.books_dictionary[books_id]
            
            if book_info['status'] == 'available':
                print(f"This book (ID: {books_id}) is already in the library (available). Please check your Book ID.")
            elif book_info['status'] == 'already issued':
                # Reset all transaction-related fields
                book_info['lender name'] = ''
                book_info['issue date'] = ''
                book_info['status'] = 'available'
                print(f"\nBook (ID: {books_id}) successfully returned and status updated to 'available'.")
            else:
                # Should not happen in this simple model, but good for robustness
                print("Unknown book status. Resetting to 'available'.")
                book_info['lender name'] = ''
                book_info['issue date'] = ''
                book_info['status'] = 'available'

        else:
            print("Error: Book ID not found in the database.")
            # return self.return_book() # Removed to prevent infinite recursion on error


# Main application loop
if __name__ == "__main__":
    
    # Initialize the Library Management System object
    try:
        my_library = LMS("list_of_books.txt", "Python's Library")
    except Exception as e:
        print(f"Could not initialize the library: {e}")
        exit()

    # Define the menu options
    press_key_list = {
        'D': "Display Books",
        'I': "Issue Book",
        'A': "Add Book",
        'R': "Return Book",
        'Q': "Quit Operation"
    }

    key_press = None
    
    # Application Loop
    while key_press != 'q':
        
        print("\n" + "#"*50)
        print(f"|{' ' * 10}WELCOME TO {my_library.library_name} LMS{' ' * 10}|")
        print("#"*50)

        # Display menu options
        for key, value in press_key_list.items():
            print(f"| Press [{key}] to {value:<35} |")
        print("#"*50)

        key_press = input("Enter your selection: ").lower().strip()

        # Handle user selection
        if key_press == 'i':
            print("\n--- Current Selection: Issue Book ---")
            my_library.issue_books()
        
        elif key_press == 'a':
            print("\n--- Current Selection: Add Book ---")
            my_library.add_books()
        
        elif key_press == 'd':
            print("\n--- Current Selection: Display Books ---")
            my_library.display_books()
        
        elif key_press == 'r':
            print("\n--- Current Selection: Return Book ---")
            my_library.return_book()
        
        elif key_press == 'q':
            print("\nThank you for using the Library Management System. Goodbye!")
            break
        
        else:
            print("\nInvalid input. Please enter one of the options: D, I, A, R, or Q.")
            continue # Skip to the next iteration of the loop