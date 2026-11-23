
import requests
from datetime import date


def fetch_book_data(isbn):
    response = requests.get(
        f"https://openlibrary.org/isbn/{isbn}.json",
        timeout=5
    )
    response.raise_for_status()
    return response.json()


def get_current_year():
    return date.today().year


def is_book_recent(publication_year):
    return publication_year >= get_current_year() - 5
