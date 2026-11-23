import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from django.core.management import execute_from_command_line

def home(request):
    context = {
        'title': 'Мій блог',
        'year': 2026,
        'categories': ['Навчання', 'Програмування', 'Новини']
    }
    return render(request, 'index.html', context)

def posts(request):
    context = {
        'title': 'Публікації блогу',
        'count': 3,
        'posts': [
            {'name': 'Python для початківців', 'description': 'Основи мови Python та її можливості'},
            {'name': 'Вивчення Django', 'description': 'Створення вебсайтів за допомогою Django'},
            {'name': 'Робота з базами даних', 'description': 'Основи роботи з базами даних'}
        ]
    }
    return render(request, 'posts.html', context)

urlpatterns = [
    path('', home),
    path('posts/', posts),
]

if __name__ == '__main__':
    execute_from_command_line(sys.argv)