
from django.db.models import Count, Avg, Q
from library.models import Author, Category, Book, Reader


def django_operations():
    print("=== DJANGO ORM ===")

    author = Author.objects.create(
        first_name="Іван",
        last_name="Франко",
        email="franko@example.com"
    )

    category = Category.objects.create(
        name="Класика",
        description="Класична література"
    )

    book = Book.objects.create(
        title="Захар Беркут",
        isbn="9786170000001",
        publication_year=1883,
        author=author
    )

    book.categories.add(category)

    reader = Reader.objects.create(
        first_name="Олег",
        last_name="Петренко",
        email="oleg@example.com",
        favorite_book=book
    )

    print("Створено автора:", author)
    print("Створено книгу:", book)
    print("Створено читача:", reader)

    books = Book.objects.filter(publication_year__gte=1900)
    print("Книги після 1900 року:", list(books))

    books = Book.objects.exclude(status="borrowed")
    print("Книги, які не видані:", list(books))

    books = Book.objects.filter(
        Q(publication_year__lt=1900) | Q(status="available")
    )
    print("Книги за умовою OR:", list(books))

    statistics = Book.objects.aggregate(
        average_year=Avg("publication_year")
    )
    print("Середній рік видання:", statistics)

    authors = Author.objects.annotate(
        books_count=Count("books")
    )

    for item in authors:
        print(item, "Кількість книг:", item.books_count)

    books = Book.objects.select_related("author").prefetch_related("categories")

    for item in books:
        print(
            item.title,
            item.author,
            list(item.categories.all())
        )

    book.title = "Захар Беркут (оновлене видання)"
    book.save()
    print("Оновлена книга:", book.title)

    book.delete()
    print("Книгу видалено")


if __name__ == "__main__":
    django_operations()
