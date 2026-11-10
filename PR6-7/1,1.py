
from flask import Flask, request, render_template_string, redirect, url_for, abort


app = Flask(__name__)


BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ title }}</h1>
    <nav>
        <a href="{{ url_for('index') }}">Головна</a> |
        <a href="{{ url_for('post_list') }}">Публікації</a> |
        <a href="{{ url_for('search') }}">Пошук</a>
    </nav>
    <hr>
    {{ content | safe }}
</body>
</html>
"""


posts_db = [
    {"id": 1, "title": "Вступ до Python", "content": "Python — потужна мова...", "author": "Іван"},
    {"id": 2, "title": "Flask для початківців", "content": "Flask — мікрофреймворк...", "author": "Марія"},
    {"id": 3, "title": "REST API", "content": "REST — архітектурний стиль...", "author": "Петро"},
]

next_id = 4


@app.route("/")
def index():
    content = "<p>Вітаємо на головній сторінці!</p>"
    return render_template_string(BASE_TEMPLATE, title="Головна", content=content)


@app.route("/posts")
def post_list():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 10

    start = (page - 1) * per_page
    end = start + per_page
    posts = posts_db[start:end]

    content = "<h2>Список публікацій</h2>"
    for post in posts:
        content += f'<p><a href="/posts/{post["id"]}">{post["title"]}</a></p>'

    return render_template_string(BASE_TEMPLATE, title="Публікації", content=content)


@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    post = next((p for p in posts_db if p["id"] == post_id), None)

    if post is None:
        abort(404)

    content = f"""
    <h2>{post['title']}</h2>
    <p>{post['content']}</p>
    <p>Автор: {post['author']}</p>
    """
    return render_template_string(BASE_TEMPLATE, title="Деталі публікації", content=content)


@app.route("/posts/create", methods=["GET", "POST"])
def post_create():
    global next_id

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content_text = request.form.get("content", "").strip()
        author = request.form.get("author", "").strip()

        if not title or not content_text or not author:
            return "Заповніть усі поля!"

        post = {
            "id": next_id,
            "title": title,
            "content": content_text,
            "author": author
        }

        posts_db.append(post)
        next_id += 1

        return redirect(url_for("post_detail", post_id=post["id"]))

    content = """
    <h2>Створення публікації</h2>
    <form method="POST">
        <p>Назва: <input type="text" name="title" required></p>
        <p>Текст: <textarea name="content" required></textarea></p>
        <p>Автор: <input type="text" name="author" required></p>
        <button type="submit">Створити</button>
    </form>
    """

    return render_template_string(BASE_TEMPLATE, title="Нова публікація", content=content)


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()

    results = [p for p in posts_db if query.lower() in p["title"].lower()]

    content = f"<h2>Результати пошуку: {query}</h2>"

    for post in results:
        content += f'<p><a href="/posts/{post["id"]}">{post["title"]}</a></p>'

    if not results:
        content += "<p>Нічого не знайдено.</p>"

    return render_template_string(BASE_TEMPLATE, title="Пошук", content=content)


@app.route("/archive/<int:year>/<int:month>")
def archive(year, month):
    if month < 1 or month > 12:
        abort(404)

    content = f"<p>Архів публікацій за {month}.{year}</p>"
    return render_template_string(BASE_TEMPLATE, title="Архів", content=content)


@app.route("/user/<string:username>")
def user_profile(username):
    content = f"<p>Профіль користувача: {username}</p>"
    return render_template_string(BASE_TEMPLATE, title="Профіль", content=content)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
