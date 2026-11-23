
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


class LibraryError(Exception):
    pass


class BookNotFoundError(LibraryError):
    pass


class BookAlreadyBorrowedError(LibraryError):
    pass


class ReaderNotFoundError(LibraryError):
    pass


class InvalidDataError(LibraryError):
    pass


class LoggingMeta(type):

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)

        message = (
            f"[{datetime.now()}] "
            f"Створено об'єкт класу {cls.__name__}"
        )

        print(message)

        with open("library.log", "a", encoding="utf-8") as file:
            file.write(message + "\n")

        return instance


def validate_text(func):

    def wrapper(self, value):
        if not isinstance(value, str) or not value.strip():
            raise InvalidDataError("Текст не може бути порожнім!")

        return func(self, value.strip())

    return wrapper


def validate_year(func):

    def wrapper(self, year):
        if not isinstance(year, int) or not 0 < year <= 2026:
            raise InvalidDataError("Некоректний рік видання!")

        return func(self, year)

    return wrapper


class Author(metaclass=LoggingMeta):

    def __init__(self, name):
        self.set_name(name)

    @validate_text
    def set_name(self, name):
        self.name = name


class Book(metaclass=LoggingMeta):

    def __init__(self, title, author, year):
        self.set_title(title)
        self.author = author
        self.set_year(year)
        self.is_borrowed = False

    @validate_text
    def set_title(self, title):
        self.title = title

    @validate_year
    def set_year(self, year):
        self.year = year

    def __str__(self):
        status = "Видана" if self.is_borrowed else "Доступна"

        return (
            f"Назва: {self.title} | "
            f"Автор: {self.author.name} | "
            f"Рік: {self.year} | "
            f"Статус: {status}"
        )


class Reader(metaclass=LoggingMeta):

    def __init__(self, name, reader_id):
        self.set_name(name)
        self.reader_id = reader_id
        self.borrowed_books = []

    @validate_text
    def set_name(self, name):
        self.name = name

    def __str__(self):
        return f"Читач: {self.name}, ID: {self.reader_id}"


class BookFactory:

    @staticmethod
    def create_book(title, author, year):
        return Book(title, author, year)


class LibraryObserver:

    def update(self, message):
        print(f"[ПОВІДОМЛЕННЯ] {message}")


class EventManager:

    def __init__(self):
        self.observers = []

    def subscribe(self, observer):
        self.observers.append(observer)

    def notify(self, message):
        for observer in self.observers:
            observer.update(message)


class SingletonMeta(LoggingMeta):

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with SingletonMeta._lock:
            if cls not in SingletonMeta._instances:
                SingletonMeta._instances[cls] = (
                    super().__call__(*args, **kwargs)
                )

            return SingletonMeta._instances[cls]


class Library(metaclass=SingletonMeta):

    def __init__(self):
        self.books = []
        self.readers = []
        self.lock = threading.RLock()

        self.events = EventManager()
        self.events.subscribe(LibraryObserver())

    def add_book(self, book):
        with self.lock:
            self.books.append(book)

        self.events.notify(f"Додано книгу: {book.title}")

    def add_reader(self, reader):
        with self.lock:
            self.readers.append(reader)

        self.events.notify(f"Додано читача: {reader.name}")

    def get_books(self):
        with self.lock:
            return list(self.books)

    def find_book(self, title):
        with self.lock:
            for book in self.books:
                if book.title.lower() == title.lower():
                    return book

        raise BookNotFoundError("Книгу не знайдено!")

    def borrow_book(self, title, reader_id):
        with self.lock:

            book = next(
                (b for b in self.books
                 if b.title.lower() == title.lower()),
                None
            )

            if book is None:
                raise BookNotFoundError("Книгу не знайдено!")

            reader = next(
                (r for r in self.readers
                 if r.reader_id == reader_id),
                None
            )

            if reader is None:
                raise ReaderNotFoundError("Читача не знайдено!")

            if book.is_borrowed:
                raise BookAlreadyBorrowedError(
                    "Книга вже видана!"
                )

            book.is_borrowed = True
            reader.borrowed_books.append(book)

        self.events.notify(
            f"Книгу '{title}' видано читачу {reader.name}"
        )

    def return_book(self, title, reader_id):
        with self.lock:

            reader = next(
                (r for r in self.readers
                 if r.reader_id == reader_id),
                None
            )

            if reader is None:
                raise ReaderNotFoundError("Читача не знайдено!")

            book = next(
                (b for b in self.books
                 if b.title.lower() == title.lower()),
                None
            )

            if book is None:
                raise BookNotFoundError("Книгу не знайдено!")

            if book not in reader.borrowed_books:
                raise BookNotFoundError(
                    "Ця книга не видана даному читачу!"
                )

            book.is_borrowed = False
            reader.borrowed_books.remove(book)

        self.events.notify(f"Книгу '{title}' повернуто")


def search_book(library, title):
    try:
        book = library.find_book(title)
        return f"Знайдено: {book.title}"

    except LibraryError as error:
        return f"Помилка: {error}"


def borrow_book(library, title, reader_id):
    try:
        library.borrow_book(title, reader_id)
        return f"Книгу '{title}' успішно видано."

    except LibraryError as error:
        return f"Помилка: {error}"


def run_tests(library):

    print("\n===== ТЕСТУВАННЯ ПОТОКІВ =====")

    tasks = [
        ("search", "Кобзар", 1),
        ("search", "Захар Беркут", 2),
        ("borrow", "Кобзар", 1),
        ("borrow", "Кобзар", 2),
        ("search", "Кобзар", 1),
        ("search", "Захар Беркут", 2)
    ]

    def execute_task(task):
        action, title, reader_id = task

        if action == "search":
            return search_book(library, title)

        return borrow_book(library, title, reader_id)

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(execute_task, tasks))

    for result in results:
        print(result)

    print("\nРезультат роботи потоків:")

    for book in library.get_books():
        print(book)


def main():

    library = Library()

    author1 = Author("Тарас Шевченко")
    author2 = Author("Іван Франко")

    book1 = BookFactory.create_book(
        "Кобзар", author1, 1840
    )

    book2 = BookFactory.create_book(
        "Захар Беркут", author2, 1883
    )

    reader1 = Reader("Олександр", 1)
    reader2 = Reader("Марія", 2)

    library.add_book(book1)
    library.add_book(book2)

    library.add_reader(reader1)
    library.add_reader(reader2)

    while True:

        print("\n===== БІБЛІОТЕЧНА СИСТЕМА =====")
        print("1. Переглянути всі книги")
        print("2. Взяти книгу")
        print("3. Повернути книгу")
        print("4. Переглянути читачів")
        print("5. Знайти книгу")
        print("6. Тестування багатопоточності")
        print("0. Вихід")

        choice = input("Оберіть дію: ")

        try:

            if choice == "1":
                for book in library.get_books():
                    print(book)

            elif choice == "2":
                title = input("Назва книги: ")
                reader_id = int(input("ID читача: "))

                library.borrow_book(title, reader_id)

            elif choice == "3":
                title = input("Назва книги: ")
                reader_id = int(input("ID читача: "))

                library.return_book(title, reader_id)

            elif choice == "4":
                with library.lock:
                    for reader in library.readers:
                        print(reader)

            elif choice == "5":
                title = input("Назва книги: ")
                print(library.find_book(title))

            elif choice == "6":
                run_tests(library)

            elif choice == "0":
                print("Завершення роботи програми.")
                break

            else:
                print("Невідома команда!")

        except (LibraryError, ValueError) as error:
            print(f"Помилка: {error}")


if __name__ == "__main__":
    main()
