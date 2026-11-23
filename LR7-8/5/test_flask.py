
import pytest
from sqlalchemy.exc import IntegrityError

from conftest import flask_module


def test_flask_author_creation(flask_author):
    assert flask_author.first_name == "Тарас"
    assert flask_author.last_name == "Шевченко"


def test_flask_book_relationship(flask_book, flask_author):
    assert flask_book.title == "Кобзар"
    assert flask_book.author.id == flask_author.id


def test_flask_client(flask_client):
    response = flask_client.get("/")
    assert response.status_code == 200
    assert "Бібліотека працює!" in response.get_data(as_text=True)


def test_flask_unique_email(flask_app, flask_author):
    db = flask_module.db

    duplicate = flask_module.Author(
        first_name="Інший",
        last_name="Автор",
        email=flask_author.email
    )

    db.session.add(duplicate)

    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()
