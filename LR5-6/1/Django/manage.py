import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

from django.conf import settings
from django.http import HttpResponse
from django.urls import path
from django.core.management import execute_from_command_line

def home(request):
    return HttpResponse("<h1>Головна сторінка блогу</h1>")

def posts(request):
    return HttpResponse("<h1>Публікації блогу</h1>")

urlpatterns = [
    path('', home),
    path('posts/', posts),
]

if __name__ == '__main__':
    execute_from_command_line(sys.argv)