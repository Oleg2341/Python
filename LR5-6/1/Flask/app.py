import os
from flask import Flask, render_template_string

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')

@app.route('/')
def home():
    return render_template_string("<h1>Головна сторінка блогу</h1>")

@app.route('/posts/')
def posts():
    return render_template_string("<h1>Публікації блогу</h1>")

if __name__ == '__main__':
    app.run(debug=True)