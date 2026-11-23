import os
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')

@app.context_processor
def inject_year():
    return {'year': datetime.now().year}

@app.route('/')
def home():
    context = {
        'title': 'Мій блог',
        'categories': ['Навчання', 'Програмування', 'Новини']
    }
    return render_template('index.html', **context)

@app.route('/posts/')
def posts():
    context = {
        'title': 'Публікації',
        'posts': [
            {'name': 'Python для початківців', 'description': 'Основи мови Python'},
            {'name': 'Вивчення Django', 'description': 'Створення вебсайтів'},
            {'name': 'Бази даних', 'description': 'Робота з базами даних'}
        ]
    }
    return render_template('posts.html', **context)

if __name__ == '__main__':
    app.run(debug=True)