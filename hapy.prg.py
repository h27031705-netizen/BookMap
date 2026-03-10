import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

# Sample book database
# added "rack" field to track physical location
books = [
    {"title": "Atomic Habits", "author": "James Clear", "genre": "Self-help", "year": 2018, "copies": 6, "rack": 1},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy", "year": 1937, "copies": 4, "rack": 2},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Classic Romance", "year": 1813, "copies": 3, "rack": 2},
    {"title": "The Alchemist", "author": "Paulo Coelho", "genre": "Adventure Fiction", "year": 1988, "copies": 5, "rack": 3},
    {"title": "Wings of Fire", "author": "A.P.J. Abdul Kalam", "genre": "Autobiography", "year": 1999, "copies": 7, "rack": 4},
    {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "genre": "Fantasy", "year": 1997, "copies": 8, "rack": 1},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Classic Fiction", "year": 1960, "copies": 4, "rack": 3},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Classic", "year": 1925, "copies": 3, "rack": 4},
    {"title": "1984", "author": "George Orwell", "genre": "Dystopian Fiction", "year": 1949, "copies": 5, "rack": 5},
    {"title": "Think and Grow Rich", "author": "Napoleon Hill", "genre": "Self-help", "year": 1937, "copies": 6, "rack": 5}
]

# MAIN WINDOW
root = tk.Tk()
root.title("Library Book Search System")
root.attributes('-fullscreen', True)
root.configure(bg="#F0E6FA")


# ---------- USER SEARCH WINDOW ----------
def open_user():
    user_window = tk.Toplevel(root)
    user_window.title("Book Search")
    user_window.attributes('-fullscreen', True)
    user_window.configure(bg="#F0E6FA")

    tk.Label(user_window, text="Search Book by Title or Author", font=("Arial", 24, "bold"), bg="#F0E6FA", fg="#4B0082").pack(pady=30)

    book_entry = tk.Entry(user_window, width=40, font=("Arial", 18), justify='center')
    book_entry.pack(pady=20)

    def search_book():
        query = book_entry.get().lower()

        if not query:
            messagebox.showwarning("Input Required", "⚠ Please enter a book title or author name to search.")
            return

        found_books = []
        for book in books:
            if query in book["title"].lower() or query in book["author"].lower():
                found_books.append(book)

        if found_books:
            result_message = "✓ BOOK(S) FOUND IN THE LIBRARY!\n\n"
            for book in found_books:
                result_message += (
                    f"Title: {book['title']}\n"
                    f"Author: {book['author']}\n"
                    f"Genre: {book['genre']}\n"
                    f"Year: {book['year']}\n"
                    f"Copies Available: {book['copies']}\n"
                    f"Rack Location: {book.get('rack', 'N/A')}\n\n"
                )
            messagebox.showinfo("Search Results", result_message)
        else:
            messagebox.showerror("Not Found", "✗ Book not found in the library.\n\nTry searching by:\n• Book Title (e.g., 'Python Basics')\n• Author Name (e.g., 'John Smith')")


    tk.Button(user_window, text="Search", command=search_book, bg="#6A5ACD", fg="white", font=("Arial", 16, "bold"), width=20, height=2).pack(pady=20)
    tk.Button(user_window, text="Close", command=user_window.destroy, bg="#9370DB", fg="white", font=("Arial", 16, "bold"), width=20, height=2).pack(pady=10)


# ---------- LIBRARIAN DASHBOARD ----------
def open_librarian():
    lib_window = tk.Toplevel(root)
    lib_window.title("Librarian Dashboard")
    lib_window.attributes('-fullscreen', True)
    lib_window.configure(bg="#F0E6FA")

    tk.Label(lib_window, text="Library Dashboard", font=("Arial", 22, "bold"), bg="#F0E6FA").pack(pady=20)

    columns = ("Book Name", "Author", "Copies Available", "Rack")

    tree = ttk.Treeview(lib_window, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)

    for book in books:
        tree.insert("", tk.END, values=(book["title"], book["author"], book["copies"], book.get("rack", "")))

    tree.pack(pady=20)

    # function to refresh the tree view after moving books
    def refresh_tree():
        for row in tree.get_children():
            tree.delete(row)
        for b in books:
            tree.insert("", tk.END, values=(b["title"], b["author"], b["copies"], b.get("rack", "")))

    # button to move book between racks
    def move_book():
        title = tk.simpledialog.askstring("Move Book", "Enter exact book title to move:")
        if not title:
            return
        for b in books:
            if b["title"].lower() == title.lower():
                new_rack = tk.simpledialog.askinteger("Move Book", f"Current rack {b.get('rack','?')}. Enter new rack number:")
                if new_rack is None:
                    return
                b["rack"] = new_rack
                messagebox.showinfo("Success", f"'{b['title']}' moved to rack {new_rack}.")
                refresh_tree()
                return
        messagebox.showerror("Error", "Book not found.")

    move_button = tk.Button(lib_window, text="Move Book", command=move_book, bg="#6A5ACD", fg="white", font=("Arial", 14, "bold"))
    move_button.pack(pady=10)

    total_books = sum(book["copies"] for book in books)

    tk.Label(lib_window, text=f"Total Books in Library: {total_books}",
             font=("Arial", 16, "bold"), bg="#F0E6FA").pack(pady=20)

    tk.Button(lib_window, text="Close", command=lib_window.destroy).pack(pady=10)


# ---------- HOME PAGE ----------
title = tk.Label(root, text="Library Book Search System",
                 font=("Arial", 28, "bold"), bg="#F0E6FA")
title.pack(pady=50)

tk.Button(root, text="User", width=25, height=3, command=open_user, font=("Arial", 16, "bold"), bg="#6A5ACD", fg="white").pack(pady=15)

tk.Button(root, text="Librarian", width=25, height=3, command=open_librarian, font=("Arial", 16, "bold"), bg="#9370DB", fg="white").pack(pady=15)

tk.Button(root, text="Exit", width=25, height=3, command=root.quit, font=("Arial", 16, "bold"), bg="#C77DDD", fg="white").pack(pady=20)


root.mainloop()