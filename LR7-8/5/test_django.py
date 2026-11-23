
import pytest
from django.db import IntegrityError, transaction
from library.models import Author, Book, Reader


def test_author_creation(django_author):
    assert django_author.first_name == "Іван"
    assert django_author.last_name == "Франко"


def test_book_string(django_book):
    assert str(django_book) == "Захар Беркут"


def test_book_default_status(django_book):
    assert django_book.status == "available"


def test_book_relationships(django_book, django_reader):
    assert django_book.author.first_name == "Іван"
    assert django_reader.favorite_book == django_book
    assert django_book in django_book.categories.first().books.all()


def test_reader_book_set_null(django_reader, django_book):
    book_id = django_book.id

    django_book.delete()
    django_reader.refresh_from_db()

    assert django_reader.favorite_book is None


def test_author_unique_email(django_author):
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Author.objects.create(
                first_name="Інший",
                last_name="Автор",
                email=django_author.email
            )


@pytest.mark.parametrize(
    "title, expected",
    [
        ("Кобзар", "Кобзар"),
        ("Захар Беркут", "Захар Беркут"),
        ("Лісова пісня", "Лісова пісня"),
    ]
)
def test_book_title(django_author, title, expected):
    book = Book.objects.create(
        title=title,
        isbn=f"ISBN-{len(title)}-{ord(title[0])}",
        publication_year=1900,
        author=django_author
    )

    assert book.title == expected
