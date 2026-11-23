
import importlib.util
import sys
from pathlib import Path

import pytest
from django.contrib.auth import get_user_model
from library.models import Author, Book, Category, Reader


spec = importlib.util.spec_from_file_location(
    "flask_library_app",
    Path(__file__).resolve().parents[1] / "3.py"
)

flask_module = importlib.util.module_from_spec(spec)
sys.modules["flask_library_app"] = flask_module
spec.loader.exec_module(flask_module)


@pytest.fixture
def django_user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="testuser",
        password="testpassword123"
    )


@pytest.fixture
def django_client(client, django_user):
    return client


@pytest.fixture
def django_author(db):
    return Author.objects.create(
        first_name="Іван",
        last_name="Франко",
        email="franko_test@example.com"
    )


@pytest.fixture
def django_category(db):
    return Category.objects.create(name="Фантастика")


@pytest.fixture
def django_book(django_author, django_category):
    book = Book.objects.create(
        title="Захар Беркут",
        isbn="9786171111111",
        publication_year=1883,
        author=django_author
    )
    book.categories.add(django_category)
    return book


@pytest.fixture
def django_reader(django_book):
    return Reader.objects.create(
        first_name="Олег",
        last_name="Петренко",
        email="reader_test@example.com",
        favorite_book=django_book
    )


@pytest.fixture
def flask_app():
    app = flask_module.app
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite://"
    )

    with app.app_context():
        flask_module.db.create_all()
        yield app
        flask_module.db.session.remove()
        flask_module.db.drop_all()


@pytest.fixture
def flask_client(flask_app):
    return flask_app.test_client()


@pytest.fixture
def flask_author(flask_app):
    db = flask_module.db
    author = flask_module.Author(
        first_name="Тарас",
        last_name="Шевченко",
        email="taras_test@example.com"
    )
    db.session.add(author)
    db.session.commit()
    return author


@pytest.fixture
def flask_book(flask_author):
    db = flask_module.db
    book = flask_module.Book(
        title="Кобзар",
        isbn="9786172222222",
        publication_year=1840,
        author_id=flask_author.id
    )
    db.session.add(book)
    db.session.commit()
    return book
