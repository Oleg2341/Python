
from unittest.mock import patch, MagicMock

from library.services import fetch_book_data, is_book_recent


def test_fetch_book_data_mock():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "title": "Кобзар",
        "publish_date": "1840"
    }

    with patch("library.services.requests.get", return_value=mock_response) as mock_get:
        result = fetch_book_data("9786175851234")

    assert result["title"] == "Кобзар"
    mock_get.assert_called_once_with(
        "https://openlibrary.org/isbn/9786175851234.json",
        timeout=5
    )
    mock_response.raise_for_status.assert_called_once_with()


def test_is_book_recent_mock():
    with patch("library.services.get_current_year", return_value=2026) as mock_year:
        result = is_book_recent(2023)

    assert result is True
    mock_year.assert_called_once_with()
