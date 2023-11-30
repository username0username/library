import sqlite3
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QTextBrowser

class Book:
    def __init__(self, id, title, author):
        self.id = id
        self.title = title
        self.author = author

class Library:
    def __init__(self):
        self.db_connection = sqlite3.connect("lib.db")
        self.create_table()

    def create_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS books 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                          title TEXT, author TEXT)''')
        self.db_connection.commit()

    def add_book(self, title, author):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
        self.db_connection.commit()

    def get_all_books(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM books")
        all_books = cursor.fetchall()
        return [Book(book[0], book[1], book[2]) for book in all_books]

    def search_book(self, title):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM books WHERE title=?", (title,))
        found_books = cursor.fetchall()
        return [Book(book[0], book[1], book[2]) for book in found_books]

    def remove_book(self, book_id):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        self.db_connection.commit()

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.library = Library()

        self.setWindowTitle("Библиотека")
        self.setFixedSize(600, 700)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.title_label = QLabel("Название книги:")
        self.title_input = QLineEdit()

        self.author_label = QLabel("Автор:")
        self.author_input = QLineEdit()

        self.add_button = QPushButton("Добавить книгу")
        self.add_button.clicked.connect(self.add_book)

        self.search_label = QLabel("Поиск по названию:")
        self.search_input = QLineEdit()

        self.search_button = QPushButton("Найти книгу")
        self.search_button.clicked.connect(self.search_book)

        self.remove_label = QLabel("Удалить книгу по ID:")
        self.remove_input = QLineEdit()

        self.remove_button = QPushButton("Удалить книгу")
        self.remove_button.clicked.connect(self.remove_book)

        self.books_label = QLabel("Все книги:")
        self.books_display = QTextBrowser()

        self.messages_label = QLabel("Сообщения:")
        self.messages_display = QTextBrowser()

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.title_input)
        self.layout.addWidget(self.author_label)
        self.layout.addWidget(self.author_input)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.search_label)
        self.layout.addWidget(self.search_input)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.remove_label)
        self.layout.addWidget(self.remove_input)
        self.layout.addWidget(self.remove_button)
        self.layout.addWidget(self.books_label)
        self.layout.addWidget(self.books_display)
        self.layout.addWidget(self.messages_label)
        self.layout.addWidget(self.messages_display)

        self.central_widget.setLayout(self.layout)

        self.show_all_books()

    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()

        if title and author:
            self.library.add_book(title, author)
            self.messages_display.append(f"Книга '{title}' успешно добавлена в библиотеку.")
            self.show_all_books()
        else:
            self.messages_display.append("Пожалуйста, заполните все поля.")

    def search_book(self):
        title = self.search_input.text()

        if title:
            found_books = self.library.search_book(title)

            if found_books:
                self.messages_display.append(f"Найдены книги по запросу '{title}':")
                for book in found_books:
                    self.messages_display.append(f"ID:{book.id} | '{book.title}' | {book.author}")
            else:
                self.messages_display.append(f"Книги по запросу '{title}' не найдены.")
        else:
            self.messages_display.append("Пожалуйста, введите название книги для поиска.")

    def remove_book(self):
        book_id_str = self.remove_input.text()

        try:
            book_id = int(book_id_str)
            self.library.remove_book(book_id)
            self.messages_display.append(f"Книга с ID:{book_id} успешно удалена из библиотеки.")
            self.show_all_books()
        except ValueError:
            self.messages_display.append("Введите корректный ID для удаления.")

    def show_all_books(self):
        self.books_display.clear()
        all_books = self.library.get_all_books()

        for book in all_books:
            self.books_display.append(f"ID:{book.id} | '{book.title}' | {book.author}")

if __name__ == "__main__":
    app = QApplication([])
    window = App()
    window.show()
    app.exec()
