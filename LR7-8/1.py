
from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Автор'
        verbose_name_plural = 'Автори'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name


class Book(models.Model):
    STATUS_CHOICES = [
        ('available', 'Доступна'),
        ('borrowed', 'Видана'),
        ('reserved', 'Зарезервована'),
    ]

    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    publication_year = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.PROTECT,
        related_name='books'
    )
    categories = models.ManyToManyField(
        Category,
        related_name='books'
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title


class Reader(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    registration_date = models.DateField(auto_now_add=True)
    favorite_book = models.OneToOneField(
        Book,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='favorite_of'
    )

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Читач'
        verbose_name_plural = 'Читачі'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
