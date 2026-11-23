
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from django.core.management import execute_from_command_line

class ContactForm(forms.Form):
    name = forms.CharField(
        label='Ваше ім’я',
        max_length=50,
        min_length=2
    )

    email = forms.EmailField(
        label='Електронна пошта'
    )

    topic = forms.ChoiceField(
        label='Тема повідомлення',
        choices=[
            ('question', 'Запитання'),
            ('suggestion', 'Пропозиція'),
            ('other', 'Інше')
        ]
    )

    message = forms.CharField(
        label='Ваше повідомлення',
        widget=forms.Textarea
    )

    def clean_name(self):
        name = self.cleaned_data['name']
        if any(char.isdigit() for char in name):
            raise forms.ValidationError(
                'Ім’я не повинно містити цифр.'
            )
        return name

    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message.split()) < 3:
            raise forms.ValidationError(
                'Повідомлення повинно містити мінімум 3 слова.'
            )
        return message


def home(request):
    return render(request, 'index.html', {'year': 2026})


def posts(request):
    return render(request, 'posts.html', {'year': 2026})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            messages.success(
                request,
                'Ваше повідомлення успішно надіслано!'
            )
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {
        'form': form,
        'year': 2026
    })


urlpatterns = [
    path('', home, name='home'),
    path('posts/', posts, name='posts'),
    path('contact/', contact, name='contact'),
]

if __name__ == '__main__':
    execute_from_command_line(sys.argv)
