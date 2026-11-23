
from sqlalchemy import func, or_
from sqlalchemy.exc import SQLAlchemyError
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

book_categories = db.Table(
    'book_categories',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True)

    books = db.relationship('Book', backref='author')


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(13), unique=True)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    description = db.Column(db.Text)
    language = db.Column(db.String(50), default='Українська')


class Reader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True)


def flask_operations():
    print("=== FLASK SQLALCHEMY ===")

    with app.app_context():
        db.create_all()

        try:
            author = Author(
                first_name="Тарас",
                last_name="Шевченко",
                email="shevchenko@example.com"
            )

            db.session.add(author)
            db.session.flush()

            book = Book(
                title="Кобзар",
                isbn="9786170000002",
                publication_year=1840,
                author_id=author.id
            )

            reader = Reader(
                first_name="Петро",
                last_name="Іваненко",
                email="petro@example.com"
            )

            db.session.add_all([book, reader])
            db.session.commit()

            print("Автор, книга та читач створені")

        except SQLAlchemyError:
            db.session.rollback()
            print("Помилка створення")

        books = Book.query.filter(
            Book.publication_year >= 1900
        ).all()

        print("Книги після 1900 року:", [b.title for b in books])

        books = Book.query.filter(
            Book.publication_year < 1900
        ).all()

        print("Книги до 1900 року:", [b.title for b in books])

        books = Book.query.filter(
            or_(
                Book.publication_year < 1900,
                Book.title == "Кобзар"
            )
        ).all()

        print("Книги за OR:", [b.title for b in books])

        count = db.session.query(func.count(Book.id)).scalar()
        average = db.session.query(
            func.avg(Book.publication_year)
        ).scalar()

        print("Кількість книг:", count)
        print("Середній рік видання:", average)

        book = Book.query.filter_by(title="Кобзар").first()

        if book:
            book.title = "Кобзар (оновлене видання)"
            db.session.commit()
            print("Книгу оновлено:", book.title)

            db.session.delete(book)
            db.session.commit()
            print("Книгу видалено")

        try:
            author = Author(
                first_name="Тест",
                last_name="Автор",
                email="test@example.com"
            )

            db.session.add(author)
            db.session.flush()

            raise ValueError("Тестова помилка транзакції")

            db.session.commit()

        except Exception:
            db.session.rollback()
            print("Транзакцію скасовано через помилку")


if __name__ == "__main__":
    flask_operations()
