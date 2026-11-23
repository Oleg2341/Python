import os
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')

@app.route('/')
def home():
    context = {
        'title': 'Мій блог',
        'year': 2026,
        'categories': ['Навчання', 'Програмування', 'Новини']
    }
    return render_template('index.html', **context)

@app.route('/posts/')
def posts():
    context = {
        'title': 'Публікації блогу',
        'count': 3,
        'posts': [
            {'name': 'Python для початківців', 'description': 'Основи мови Python та її можливості'},
            {'name': 'Вивчення Django', 'description': 'Створення вебсайтів за допомогою Django'},
            {'name': 'Робота з базами даних', 'description': 'Основи роботи з базами даних'}
        ]
    }
    return render_template('posts.html', **context)

if __name__ == '__main__':
    app.run(debug=True)