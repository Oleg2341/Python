
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

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

    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    books = db.relationship(
        'Book',
        secondary=book_categories,
        backref='categories'
    )

    def __repr__(self):
        return self.name


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(13), unique=True)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    description = db.Column(db.Text, default='')

    def __repr__(self):
        return self.title


class Reader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True)
    favorite_book_id = db.Column(
        db.Integer,
        db.ForeignKey('book.id'),
        unique=True,
        nullable=True
    )

    favorite_book = db.relationship('Book', backref='favorite_reader', uselist=False)

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'


@app.route('/')
def home():
    return 'Бібліотека працює!'


if __name__ == '__main__':
    app.run(debug=True)
