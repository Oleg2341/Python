
from flask import Flask, request, render_template_string, redirect, url_for, flash, abort
from datetime import datetime


app = Flask(__name__)
app.secret_key = "blog-secret-key"


LIST_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Блог</title></head>
<body>
    <h1>Публікації</h1>

    {% with messages = get_flashed_messages() %}
    {% if messages %}
        <div style="color: green;">{{ messages[0] }}</div>
    {% endif %}
    {% endwith %}

    <a href="{{ url_for('post_create') }}">+ Нова публікація</a>
    <hr>

    {% for post in posts %}
    <article>
        <h2>
            <a href="{{ url_for('post_detail', post_id=post.id) }}">
                {{ post.title }}
            </a>
        </h2>
        <p>{{ post.content[:100] }}...</p>
        <small>{{ post.author }} | {{ post.created_at }}</small>
    </article>
    <hr>
    {% endfor %}

    <p>
        {% if page > 1 %}
            <a href="{{ url_for('post_list', page=page-1) }}">Попередня</a>
        {% endif %}

        Сторінка {{ page }} з {{ total_pages }}

        {% if page < total_pages %}
            <a href="{{ url_for('post_list', page=page+1) }}">Наступна</a>
        {% endif %}
    </p>
</body>
</html>
"""


FORM_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>{{ form_title }}</title></head>
<body>
    <h1>{{ form_title }}</h1>

    <form method="POST">
        <label>Заголовок:</label><br>
        <input type="text" name="title" required style="width:400px;"><br><br>

        <label>Автор:</label><br>
        <input type="text" name="author" required><br><br>

        <label>Зміст:</label><br>
        <textarea name="content" rows="10" cols="50" required></textarea><br><br>

        <button type="submit">{{ button_text }}</button>
        <a href="{{ url_for('post_list') }}">Скасувати</a>
    </form>
</body>
</html>
"""


DETAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>{{ post.title }}</title></head>
<body>
    <h1>{{ post.title }}</h1>
    <p>{{ post.content }}</p>
    <p>Автор: {{ post.author }}</p>
    <small>Дата створення: {{ post.created_at }}</small>
    <hr>
    <a href="{{ url_for('post_list') }}">Назад до публікацій</a>
</body>
</html>
"""


posts_db = []
next_id = 1


@app.route("/posts")
def post_list():
    page = request.args.get("page", 1, type=int)

    if page is None or page < 1:
        page = 1

    per_page = 5
    total = len(posts_db)
    total_pages = max(1, (total + per_page - 1) // per_page)

    if page > total_pages:
        page = total_pages

    start = (page - 1) * per_page
    posts = posts_db[start:start + per_page]

    return render_template_string(
        LIST_TEMPLATE,
        posts=posts,
        page=page,
        total_pages=total_pages
    )


@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    post = next((p for p in posts_db if p["id"] == post_id), None)

    if post is None:
        abort(404)

    return render_template_string(DETAIL_TEMPLATE, post=post)


@app.route("/posts/create", methods=["GET", "POST"])
def post_create():
    global next_id

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not author or not content:
            flash("Заповніть усі поля!")
            return render_template_string(
                FORM_TEMPLATE,
                form_title="Нова публікація",
                button_text="Створити"
            )

        post = {
            "id": next_id,
            "title": title,
            "author": author,
            "content": content,
            "created_at": datetime.now().strftime("%d.%m.%Y %H:%M")
        }

        posts_db.append(post)
        next_id += 1

        flash("Публікацію успішно створено!")
        return redirect(url_for("post_detail", post_id=post["id"]))

    return render_template_string(
        FORM_TEMPLATE,
        form_title="Нова публікація",
        button_text="Створити"
    )


@app.errorhandler(404)
def not_found(error):
    return "Публікацію не знайдено", 404


if __name__ == "__main__":
    app.run(debug=True, port=5003)
