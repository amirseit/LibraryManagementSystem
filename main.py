import logging
from library_management import Library

# --- Main Program Entry Point ---

if __name__ == "__main__":
    # Clear existing logging handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Set up logging configuration
    logging.basicConfig(
        filename='app.log',
        level=logging.INFO,  # Logs INFO and higher levels (WARNING, ERROR, etc.)
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    library = Library()

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Delete Book")
        print("3. Search for Books")
        print("4. Display All Books")
        print("5. Change Book Status")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            library.add_book()
        elif choice == "2":
            library.delete_book()
        elif choice == "3":
            library.search_books()
        elif choice == "4":
            library.display_books()
        elif choice == "5":
            library.change_status()
        elif choice == "6":
            print("Exiting the Library Management System. Goodbye!")
            logging.shutdown()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
            logging.warning(f"Invalid menu selection: '{choice}'")