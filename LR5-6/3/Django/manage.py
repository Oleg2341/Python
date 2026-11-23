import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from django.core.management import execute_from_command_line
from datetime import datetime

def home(request):
    context = {
        'title': 'Мій блог',
        'year': datetime.now().year,
        'categories': ['Навчання', 'Програмування', 'Новини']
    }
    return render(request, 'index.html', context)

def posts(request):
    context = {
        'title': 'Публікації',
        'year': datetime.now().year,
        'posts': [
            {'name': 'Python для початківців', 'description': 'Основи мови Python'},
            {'name': 'Вивчення Django', 'description': 'Створення вебсайтів'},
            {'name': 'Бази даних', 'description': 'Робота з базами даних'}
        ]
    }
    return render(request, 'posts.html', context)

urlpatterns = [
    path('', home, name='home'),
    path('posts/', posts, name='posts'),
]

if __name__ == '__main__':
    execute_from_command_line(sys.argv)