


import os
import sys
from tabulate import tabulate
from datetime import datetime

# Function to update the status of a book
def update_status(new_status, book_id):
    new_file = []
    books_info = get_books_info('src/BookList.txt', {})
    with open('src/BookList.txt', 'r') as file:
        for line in file:
            # print(line)
            # print(f":{line[:4]}:")
            if line[:3] == book_id:
                # print("Found!")
                new_file.append(line.replace(books_info[book_id][-1], new_status))
                # Update the books_info dictionary with the new status
                books_info[book_id][-1] = new_status
            else:
                new_file.append(line)
    print(new_file)
    with open('src/BookList.txt', 'w') as file:
        file.writelines(new_file)

# Function which gets the last book ID from the file
def get_last_id(directory):
    try:
        with open(directory) as file:
            last_line = file.readlines()
            return last_line[-1][:4] if last_line else '0000'
    except FileNotFoundError:
        with open(directory, 'a'):
            return '0000'


# Function to get book information from th file
def get_books_info(directory, books_info):
    if not os.path.exists(directory):
        # Creates the directory if it doesn't exist
        os.makedirs(os.path.dirname(directory), exist_ok=True)

        # Creates the file
        with open(directory, 'w'):
            pass

    with open(directory, 'r') as file:
        for line in file:

            # Splits the line into parts using ' - ' as the separator
            parts = line.strip().split(' - ')

            # Checks if there are at least five parts
            if len(parts) >= 5:
                book_id, book_title, book_author, book_genre, status = parts[:5]
                books_info[book_id] = [book_title, book_author, book_genre, status]
            else:
                print(f"Invalid data in the file: {line}")

    return books_info

# Function to display the book list
def display_book_list():
    try:
        with open('src/BookList.txt') as book_list_file:
            book_list = [line.split(' - ') for line in book_list_file]
            headers = ["Book ID", "Book Title", "Book Author", "Book Genre", "Book Status"]
            print(tabulate(book_list, headers=headers))
    except FileNotFoundError:
        print("There is no book registered in this library.")


# Function to borrow a book
def borrow_book():
    borrow_id = input("Enter the Book ID to borrow: ").strip()
    books_info = get_books_info('src/BookList.txt', {})
    if borrow_id in books_info:
        # book_title, book_author, status = books_info[borrow_id]
        if books_info[borrow_id][-1] == 'not taken':
            update_status('taken', borrow_id)
            print(f'The book with ID {borrow_id} has been successfully borrowed.')
        else:
            print(f'The book with ID {borrow_id} has already been borrowed.')
    else:
        print(f'No book found with ID: {borrow_id}')

# Function to return a book
def return_book():
    return_id = input("Enter the Book ID to return: ").strip()
    books_info = get_books_info('src/BookList.txt', {})
    if return_id in books_info:
        if books_info[return_id][-1] == 'taken':
            update_status('not taken', return_id)
            print(f'The book with ID {return_id} has been successfully returned.')
        else:
            print(f'The book with ID {return_id} has not been borrowed before.')
    else:
        print(f'No book found with ID: {return_id}')


# Function to edit a book
def edit_book():
    edit_id = input("Enter the Book ID to edit: ").strip()
    books_info = get_books_info('src/BookList.txt', {})

    if edit_id in books_info:
        print("Current Book Information:")
        print(f'Book Title: {books_info[edit_id][0]}\nBook Author: {books_info[edit_id][1]}\nBook Genre: {books_info[edit_id][2]}')

        new_title = input("Enter the new Book Title: ").title().strip() or books_info[edit_id][0]
        new_author = input("Enter the new Book Author: ").title().strip() or books_info[edit_id][1]
        new_genre = input("Enter the new Genre of Book: ").title().strip() or books_info[edit_id][2]

        books_info[edit_id] = [new_title, new_author, new_genre, books_info[edit_id][-1]]

        # Updates the file with the new information
        update_file(books_info)

        print(f'The book with ID {edit_id} has been successfully edited.')
    else:
        print(f'No book found with this ID: {edit_id}')
    
# Function to update the file with the edited book information
def update_file(books_info):
    with open('src/BookList.txt', 'w') as file:
        for book_id, info in books_info.items():
            file.write(f'{book_id} - {info[0]} - {info[1]} - {info[2]} - {info[3]}\n')


# Function to add a new book
def add_book():
    book_title = input("Enter the Book Title: ").title().strip()
    book_author = input("Enter the Book Author: ").title().strip()
    book_genre = input("Enter the Genre of Book: ").title().strip()

    books_info = get_books_info('src/BookList.txt', {})
    if [book_title, book_author] in [info[:2] for info in books_info.values()]:
        print("This book has already been added.")
    else:
        book_id = get_last_id('src/BookList.txt')
        if 999 > int(book_id) >= 99:
            book_id = f'{str(int(book_id)+1)}'
        elif 99 > int(book_id) >= 9:
            book_id = f'0{str(int(book_id)+1)}'
        elif int(book_id) >= 999:
            # Handle the case when you reach 1000 books (adjust as needed)
            print("Cannot add more books. Book ID limit reached.")
            return
        else:
            book_id = f'00{str(int(book_id)+1)}'
        with open('src/BookList.txt', 'a') as file:
            file.write(f'{book_id} - {book_title} - {book_author} - {book_genre} - not taken\n')
        print(f'The book with ID {book_id} has been successfully added.')

# Function to delete a book
def delete_book():
    delete_id = input("Enter the Book ID to delete: ").strip()
    books_info = get_books_info('src/BookList.txt', {})
    if delete_id in books_info:
        new_file = []
        with open('src/BookList.txt', 'r') as file:
            for line in file:
                if int(line[:4]) < int(delete_id):
                    new_file.append(line)
                elif line[:4] == delete_id:
                    pass
                elif int(line[:4]) > int(delete_id):
                    if int(line[:4]) <= 100:
                        new_file.append(line.replace(line[:4], f'0{str(int(line[:4])-1)}'))
                    elif int(line[:4]) > 100 and int(line[:4]) < 1000:
                        new_file.append(line.replace(line[:4], f'{str(int(line[:4])-1)}'))
        with open('src/BookList.txt', 'w') as file:
            file.writelines(new_file)
        print(f'The book with ID {delete_id} has been successfully deleted.')
    else:
        print(f'No book found with ID: {delete_id}')

SEARCH_CATEGORIES = {
    'title': 0,
    'author': 1,
    'genre': 2,
    'id': 3  # Add 'id' as a search category
}

def search_book():
    search_term = input("Enter the search term: ").strip().lower()
    search_category = input("Choose search category (title, author, genre, id): ").strip().lower()

    books_info = get_books_info('src/BookList.txt', {})
    matching_books = []

    for book_id, info in books_info.items():
        # Check if the search term matches the specified category
        if search_category == 'id' and search_term == book_id.lower():
            matching_books.append((book_id, info))
        elif search_term in info[SEARCH_CATEGORIES[search_category]].lower():
            matching_books.append((book_id, info))

    if matching_books:
        print("\nSearch Results: ")
        for book_id, info in matching_books:
            print(book_id, info)
    else:
        print(f'No book found with {search_category} containing "{search_term}".')



# def search_book():
    # search_id = input("Enter the Book ID to search: ").strip()
    # books_info = get_books_info('src/BookList.txt', {})
    # if search_id in books_info:
    #     print(f'Book Title: {books_info[search_id][0]}\nBook Author: {books_info[search_id][1]}\nBook Genre: {books_info[search_id][2]}\nBook Status: {books_info[search_id][3]}')
    # else:
    #     print(f'No book found with ID: {search_id}')

# Function to sort books
def sort_books():
    sort_category = input("Choose sort category (title, author, genre): ").strip().lower()
    ascending = input("Sort in ascending order? (y/n): ").strip().lower() == 'y'

    books_info = get_books_info('src/BookList.txt', {})
    sorted_books = sorted(books_info.items(), key=lambda x: x[1][SEARCH_CATEGORIES[sort_category]], reverse=not ascending)

    print("\nSorted Book List:")
    for book_id, info in sorted_books:
        print(book_id, info)



# Main function
def main():
    while True:
        print("\n<<<<<<<<<<<----Library Management System---->>>>>>>>>>>\n")
        print("1. Display Book List")
        print("2. Search for a Book")
        print("3. Borrow a Book")
        print("4. Return a Book")
        print("5. Add a New Book")
        print("6. Edit Book")
        print("7. Delete a Book")
        print("8. Sort Books")
        print("9. Exit")
        
        choice = input("\nEnter your choice (1-9): ")
        
        if choice == '1':
            display_book_list()
        elif choice == '2':
            search_book()
        elif choice == '3':
            borrow_book()
        elif choice == '4':
            return_book()
        elif choice == '5':
            add_book()
        elif choice == '6':
            edit_book()
        elif choice == '7':
            delete_book()
        elif choice == '8':
            sort_books()
        elif choice == '9':
            sys.exit()
        else:
            print("Invalid choice. Please enter a number between 1 and 10.")

if __name__ == "__main__":
    main()



# Borrowing book and their borrowed date
# def borrow_book():
    # borrow_id = input("Enter the Book ID to borrow: ").strip()
    # books_info = get_books_info('src/BookList.txt', {})
    # if borrow_id in books_info:
    #     if books_info[borrow_id][-2] == 'not taken':  # Check if the book is not already taken
    #         update_status('taken', borrow_id)
    #         borrowed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #         update_borrowed_date(borrow_id, borrowed_date)
    #         print(f'The book with ID {borrow_id} has been successfully borrowed.')
    #     else:
    #         print(f'The book with ID {borrow_id} has already been borrowed.')
    # else:
    #     print(f'No book found with ID: {borrow_id}')
# def update_borrowed_date(book_id, borrowed_date):
    # new_file = []
    # books_info = get_books_info('src/BookList.txt', {})
    # with open('src/BookList.txt', 'r') as file:
    #     for line in file:
    #         if line[:4] == book_id:
    #             new_file.append(line.replace(books_info[book_id][-2], borrowed_date))
    #             books_info[book_id][-2] = borrowed_date
    #         else:
    #             new_file.append(line)
    # with open('src/BookList.txt', 'w') as file:
    #     file.writelines(new_file)


# Returning book and their returned date
# def return_book():
    # return_id = input("Enter the Book ID to return: ").strip()
    # books_info = get_books_info('src/BookList.txt', {})
    # if return_id in books_info:
    #     if books_info[return_id][-2] == 'taken':  # Check if the book is currently borrowed
    #         update_status('not taken', return_id)
    #         returned_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #         update_returned_date(return_id, returned_date)
    #         print(f'The book with ID {return_id} has been successfully returned.')
    #     else:
    #         print(f'The book with ID {return_id} has not been borrowed before.')
    # else:
    #     print(f'No book found with ID: {return_id}')
# def update_returned_date(book_id, returned_date):
    # new_file = []
    # books_info = get_books_info('src/BookList.txt', {})
    # with open('src/BookList.txt', 'r') as file:
    #     for line in file:
    #         if line[:4] == book_id:
    #             new_file.append(line.replace(books_info[book_id][-1], returned_date))
    #             books_info[book_id][-1] = returned_date
    #         else:
    #             new_file.append(line)
    # with open('src/BookList.txt', 'w') as file:
    #     file.writelines(new_file)

















# # Example usage:
# library_system = Library()

# # Add books to the catalog
# library_system.add_book('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction')
# library_system.add_book('To Kill a Mockingbird', 'Harper Lee', 'Fiction')

# # Search for books
# search_results = library_system.search_books('author', 'Harper Lee')
# print('Search Results:', search_results)

# # Sort books by title
# library_system.sort_books('title')

# # Check out and return books
# library_system.checkout_book('The Great Gatsby', 'John Doe', '2023-01-15')
# library_system.return_book('The Great Gatsby')

# # Check for overdue books
# library_system.check_overdue_books('2023-01-20')

# # Display library summary
# library_system.library_summary()
