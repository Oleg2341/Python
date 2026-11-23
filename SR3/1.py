from flask import Flask, render_template_string, request, redirect, url_for, session, flash, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "bookstore_secret_key_2026"
app.config["DATABASE"] = "bookstore.db"


def get_db():
    db = sqlite3.connect(app.config["DATABASE"])
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER,
            category_id INTEGER,
            price REAL NOT NULL,
            description TEXT,
            FOREIGN KEY(author_id) REFERENCES authors(id),
            FOREIGN KEY(category_id) REFERENCES categories(id)
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total REAL NOT NULL,
            status TEXT DEFAULT 'Нове',
            FOREIGN KEY(user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(book_id) REFERENCES books(id)
        );
    """)

    if not db.execute("SELECT id FROM users WHERE username='admin'").fetchone():
        db.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", generate_password_hash("admin123"), "admin")
        )

    if not db.execute("SELECT id FROM authors LIMIT 1").fetchone():
        authors = ["Тарас Шевченко", "Іван Франко", "Леся Українка"]
        for name in authors:
            db.execute("INSERT INTO authors (name) VALUES (?)", (name,))

    if not db.execute("SELECT id FROM categories LIMIT 1").fetchone():
        categories = ["Класика", "Фантастика", "Навчальна література"]
        for name in categories:
            db.execute("INSERT INTO categories (name) VALUES (?)", (name,))

    if not db.execute("SELECT id FROM books LIMIT 1").fetchone():
        books = [
            ("Кобзар", 1, 1, 250, "Збірка поезій Тараса Шевченка."),
            ("Захар Беркут", 2, 1, 300, "Історична повість Івана Франка."),
            ("Лісова пісня", 3, 1, 220, "Драма-феєрія Лесі Українки.")
        ]
        db.executemany(
            "INSERT INTO books (title, author_id, category_id, price, description) VALUES (?, ?, ?, ?, ?)",
            books
        )

    db.commit()
    db.close()


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Доступ дозволено тільки адміністратору.")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated


BASE = """
<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Книжковий магазин</title>
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f3f4f6;
    color: #252525;
}
header {
    background: #26344a;
    color: white;
    padding: 20px;
}
nav {
    display: flex;
    flex-wrap: wrap;
    gap: 18px;
    align-items: center;
}
nav a {
    color: white;
    text-decoration: none;
}
nav a:hover { color: #f4c95d; }
.container {
    max-width: 1100px;
    margin: 30px auto;
    padding: 20px;
}
h1 { color: #26344a; }
.books {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 8px #00000012;
}
.card h3 { color: #26344a; }
.price {
    color: #23844c;
    font-size: 20px;
    font-weight: bold;
}
input, textarea, select {
    display: block;
    width: 100%;
    padding: 11px;
    margin: 10px 0;
    border: 1px solid #ccc;
    border-radius: 5px;
}
button, .btn {
    display: inline-block;
    background: #26344a;
    color: white;
    border: none;
    padding: 10px 16px;
    border-radius: 5px;
    cursor: pointer;
    text-decoration: none;
    margin-top: 8px;
}
button:hover, .btn:hover { background: #405878; }
.danger { background: #b83232; }
.message {
    background: #fff1c9;
    padding: 12px;
    margin: 10px 0;
    border-radius: 5px;
}
table {
    width: 100%;
    background: white;
    border-collapse: collapse;
}
td, th {
    padding: 12px;
    border: 1px solid #ddd;
    text-align: left;
}
footer {
    text-align: center;
    padding: 25px;
    color: #777;
}
</style>
</head>
<body>
<header>
    <nav>
        <strong>BOOKSTORE</strong>
        <a href="/">Головна</a>
        <a href="/cart">Кошик</a>
        <a href="/orders">Мої замовлення</a>
        <a href="/api/books">REST API</a>
        {% if session.get('role') == 'admin' %}
            <a href="/admin">Адміністрування</a>
        {% endif %}
        {% if session.get('user_id') %}
            <span>Користувач: {{ session.get('username') }}</span>
            <a href="/logout">Вийти</a>
        {% else %}
            <a href="/login">Увійти</a>
            <a href="/register">Реєстрація</a>
        {% endif %}
    </nav>
</header>
<div class="container">
    {% for message in get_flashed_messages() %}
        <div class="message">{{ message }}</div>
    {% endfor %}
    CONTENT
</div>
<footer>Онлайн-магазин книг | Навчальний проєкт Django/Flask</footer>
</body>
</html>
"""


def page(content, **kwargs):
    return render_template_string(BASE.replace("CONTENT", content), **kwargs)


@app.route("/")
def index():
    db = get_db()
    books = db.execute("""
        SELECT books.*, authors.name AS author,
        categories.name AS category
        FROM books
        LEFT JOIN authors ON books.author_id = authors.id
        LEFT JOIN categories ON books.category_id = categories.id
        ORDER BY books.id DESC
    """).fetchall()
    db.close()

    return page("""
    <h1>Каталог книг</h1>
    <p>Ласкаво просимо до нашого онлайн-магазину!</p>
    <div class="books">
    {% for book in books %}
        <div class="card">
            <h3>{{ book.title }}</h3>
            <p>Автор: {{ book.author or 'Не вказано' }}</p>
            <p>Категорія: {{ book.category or 'Не вказано' }}</p>
            <p>{{ book.description }}</p>
            <p class="price">{{ book.price }} грн</p>
            <a class="btn" href="/book/{{ book.id }}">Детальніше</a>
            <form method="POST" action="/add-to-cart/{{ book.id }}">
                <button type="submit">До кошика</button>
            </form>
        </div>
    {% else %}
        <p>Книг поки немає.</p>
    {% endfor %}
    </div>
    """, books=books)


@app.route("/book/<int:book_id>")
def book_detail(book_id):
    db = get_db()
    book = db.execute("""
        SELECT books.*, authors.name AS author,
        categories.name AS category
        FROM books
        LEFT JOIN authors ON books.author_id = authors.id
        LEFT JOIN categories ON books.category_id = categories.id
        WHERE books.id = ?
    """, (book_id,)).fetchone()
    db.close()

    if not book:
        return "Книгу не знайдено", 404

    return page("""
    <h1>{{ book.title }}</h1>
    <div class="card">
        <p>Автор: {{ book.author or 'Не вказано' }}</p>
        <p>Категорія: {{ book.category or 'Не вказано' }}</p>
        <p>{{ book.description }}</p>
        <p class="price">{{ book.price }} грн</p>
        <form method="POST" action="/add-to-cart/{{ book.id }}">
            <button type="submit">Додати до кошика</button>
        </form>
    </div>
    """, book=book)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if len(username) < 3 or len(password) < 6:
            flash("Логін має містити щонайменше 3 символи, пароль — 6.")
            return redirect(url_for("register"))

        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password))
            )
            db.commit()
            flash("Реєстрація успішна. Тепер увійдіть.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Такий користувач уже існує.")
        finally:
            db.close()

    return page("""
    <h1>Реєстрація</h1>
    <form method="POST">
        <input name="username" placeholder="Логін" required minlength="3">
        <input name="password" type="password" placeholder="Пароль" required minlength="6">
        <button>Зареєструватися</button>
    </form>
    """)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        db.close()

        if user and check_password_hash(user["password"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            flash("Ви успішно увійшли!")
            return redirect(url_for("index"))

        flash("Неправильний логін або пароль.")

    return page("""
    <h1>Вхід до системи</h1>
    <form method="POST">
        <input name="username" placeholder="Логін" required>
        <input name="password" type="password" placeholder="Пароль" required>
        <button>Увійти</button>
    </form>
    <p>Тестовий адміністратор: admin / admin123</p>
    """)


@app.route("/logout")
def logout():
    session.clear()
    flash("Ви вийшли з облікового запису.")
    return redirect(url_for("index"))


@app.route("/add-to-cart/<int:book_id>", methods=["POST"])
def add_to_cart(book_id):
    db = get_db()
    book = db.execute(
        "SELECT id FROM books WHERE id = ?", (book_id,)
    ).fetchone()
    db.close()

    if not book:
        return "Книгу не знайдено", 404

    cart = session.get("cart", {})
    cart[str(book_id)] = cart.get(str(book_id), 0) + 1
    session["cart"] = cart
    flash("Книгу додано до кошика.")
    return redirect(request.referrer or url_for("index"))


@app.route("/cart")
def cart():
    cart_data = session.get("cart", {})
    db = get_db()
    items = []
    total = 0

    for book_id, quantity in cart_data.items():
        book = db.execute(
            "SELECT * FROM books WHERE id = ?", (int(book_id),)
        ).fetchone()
        if book:
            subtotal = book["price"] * quantity
            total += subtotal
            items.append({
                "id": book["id"],
                "title": book["title"],
                "price": book["price"],
                "quantity": quantity,
                "subtotal": subtotal
            })

    db.close()

    return page("""
    <h1>Кошик покупок</h1>
    {% if items %}
    <table>
        <tr><th>Книга</th><th>Ціна</th><th>Кількість</th><th>Сума</th></tr>
        {% for item in items %}
        <tr>
            <td>{{ item.title }}</td>
            <td>{{ item.price }} грн</td>
            <td>{{ item.quantity }}</td>
            <td>{{ item.subtotal }} грн</td>
        </tr>
        {% endfor %}
    </table>
    <h3>Загальна сума: {{ total }} грн</h3>
    <form method="POST" action="/checkout">
        <button>Оформити замовлення</button>
    </form>
    <a href="/clear-cart" class="btn danger">Очистити кошик</a>
    {% else %}
        <p>Кошик порожній.</p>
    {% endif %}
    """, items=items, total=total)


@app.route("/clear-cart")
def clear_cart():
    session.pop("cart", None)
    flash("Кошик очищено.")
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["POST"])
def checkout():
    if not session.get("user_id"):
        flash("Для оформлення замовлення необхідно увійти.")
        return redirect(url_for("login"))

    cart_data = session.get("cart", {})
    if not cart_data:
        flash("Кошик порожній.")
        return redirect(url_for("cart"))

    db = get_db()
    items = []
    total = 0

    for book_id, quantity in cart_data.items():
        book = db.execute(
            "SELECT * FROM books WHERE id = ?", (int(book_id),)
        ).fetchone()

        if book and quantity > 0:
            items.append((book, quantity))
            total += book["price"] * quantity

    if not items:
        db.close()
        session.pop("cart", None)
        flash("Книги більше недоступні.")
        return redirect(url_for("cart"))

    cursor = db.execute(
        "INSERT INTO orders (user_id, total) VALUES (?, ?)",
        (session["user_id"], total)
    )
    order_id = cursor.lastrowid

    for book, quantity in items:
        db.execute("""
            INSERT INTO order_items (order_id, book_id, quantity, price)
            VALUES (?, ?, ?, ?)
        """, (order_id, book["id"], quantity, book["price"]))

    db.commit()
    db.close()

    session.pop("cart", None)
    flash("Замовлення успішно оформлено!")
    return redirect(url_for("orders"))


@app.route("/orders")
def orders():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    db = get_db()
    result = db.execute(
        "SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC",
        (session["user_id"],)
    ).fetchall()
    db.close()

    return page("""
    <h1>Мої замовлення</h1>
    <table>
        <tr><th>Номер</th><th>Сума</th><th>Статус</th></tr>
        {% for order in orders %}
        <tr>
            <td>{{ order.id }}</td>
            <td>{{ order.total }} грн</td>
            <td>{{ order.status }}</td>
        </tr>
        {% else %}
        <tr><td colspan="3">Замовлень поки немає.</td></tr>
        {% endfor %}
    </table>
    """, orders=result)


@app.route("/admin")
@admin_required
def admin():
    db = get_db()
    books = db.execute("SELECT * FROM books").fetchall()
    authors = db.execute("SELECT * FROM authors").fetchall()
    categories = db.execute("SELECT * FROM categories").fetchall()
    orders = db.execute("""
        SELECT orders.*, users.username
        FROM orders JOIN users ON orders.user_id = users.id
        ORDER BY orders.id DESC
    """).fetchall()
    db.close()

    return page("""
    <h1>Адміністративна панель</h1>
    <h2>Додавання книги</h2>
    <form method="POST" action="/admin/add">
        <input name="title" placeholder="Назва книги" required>
        <select name="author_id">
            {% for a in authors %}
                <option value="{{ a.id }}">{{ a.name }}</option>
            {% endfor %}
        </select>
        <select name="category_id">
            {% for c in categories %}
                <option value="{{ c.id }}">{{ c.name }}</option>
            {% endfor %}
        </select>
        <input name="price" type="number" min="0.01" step="0.01" placeholder="Ціна" required>
        <textarea name="description" placeholder="Опис книги"></textarea>
        <button>Додати книгу</button>
    </form>

    <h2>Керування книгами</h2>
    <table>
        <tr><th>Назва</th><th>Ціна</th><th>Дії</th></tr>
        {% for book in books %}
        <tr>
            <td>{{ book.title }}</td>
            <td>{{ book.price }} грн</td>
            <td>
                <a href="/admin/edit/{{ book.id }}">Редагувати</a>
                <form method="POST" action="/admin/delete/{{ book.id }}">
                    <button class="danger">Видалити</button>
                </form>
            </td>
        </tr>
        {% endfor %}
    </table>

    <h2>Замовлення користувачів</h2>
    <table>
        <tr><th>Номер</th><th>Користувач</th><th>Сума</th><th>Статус</th></tr>
        {% for order in orders %}
        <tr>
            <td>{{ order.id }}</td>
            <td>{{ order.username }}</td>
            <td>{{ order.total }} грн</td>
            <td>{{ order.status }}</td>
        </tr>
        {% endfor %}
    </table>
    """, books=books, authors=authors, categories=categories, orders=orders)


@app.route("/admin/add", methods=["POST"])
@admin_required
def add_book():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "")
    try:
        price = float(request.form.get("price", ""))
        author_id = int(request.form.get("author_id", ""))
        category_id = int(request.form.get("category_id", ""))
        if not title or price <= 0:
            raise ValueError
    except ValueError:
        flash("Перевірте правильність введених даних.")
        return redirect(url_for("admin"))

    db = get_db()
    author = db.execute("SELECT id FROM authors WHERE id=?", (author_id,)).fetchone()
    category = db.execute("SELECT id FROM categories WHERE id=?", (category_id,)).fetchone()

    if not author or not category:
        db.close()
        flash("Вибраного автора або категорію не знайдено.")
        return redirect(url_for("admin"))

    db.execute("""
        INSERT INTO books (title, author_id, category_id, price, description)
        VALUES (?, ?, ?, ?, ?)
    """, (title, author_id, category_id, price, description))
    db.commit()
    db.close()
    flash("Книгу додано.")
    return redirect(url_for("admin"))


@app.route("/admin/edit/<int:book_id>", methods=["GET", "POST"])
@admin_required
def edit_book(book_id):
    db = get_db()
    book = db.execute("SELECT * FROM books WHERE id=?", (book_id,)).fetchone()

    if not book:
        db.close()
        return "Книгу не знайдено", 404

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        try:
            price = float(request.form.get("price", ""))
            if not title or price <= 0:
                raise ValueError
        except ValueError:
            db.close()
            flash("Перевірте назву та ціну.")
            return redirect(url_for("edit_book", book_id=book_id))

        db.execute("""
            UPDATE books SET title=?, price=?, description=?
            WHERE id=?
        """, (title, price, request.form.get("description", ""), book_id))
        db.commit()
        db.close()
        flash("Дані книги оновлено.")
        return redirect(url_for("admin"))

    db.close()
    return page("""
    <h1>Редагування книги</h1>
    <form method="POST">
        <input name="title" value="{{ book.title }}" required>
        <input name="price" type="number" step="0.01" min="0.01" value="{{ book.price }}" required>
        <textarea name="description">{{ book.description }}</textarea>
        <button>Зберегти зміни</button>
    </form>
    """, book=book)


@app.route("/admin/delete/<int:book_id>", methods=["POST"])
@admin_required
def delete_book(book_id):
    db = get_db()
    used = db.execute(
        "SELECT id FROM order_items WHERE book_id=? LIMIT 1", (book_id,)
    ).fetchone()

    if used:
        db.close()
        flash("Книгу не можна видалити: вона є в замовленнях.")
        return redirect(url_for("admin"))

    db.execute("DELETE FROM books WHERE id=?", (book_id,))
    db.commit()
    db.close()
    flash("Книгу видалено.")
    return redirect(url_for("admin"))


# REST API

@app.route("/api/books", methods=["GET", "POST"])
def api_books():
    db = get_db()

    if request.method == "GET":
        books = db.execute("SELECT * FROM books").fetchall()
        result = [dict(book) for book in books]
        db.close()
        return jsonify(result)

    if session.get("role") != "admin":
        db.close()
        return jsonify({"error": "Потрібні права адміністратора"}), 403

    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()

    try:
        price = float(data.get("price", 0))
        author_id = int(data.get("author_id"))
        category_id = int(data.get("category_id"))
        if not title or price <= 0:
            raise ValueError
    except (ValueError, TypeError):
        db.close()
        return jsonify({"error": "Некоректні дані книги"}), 400

    author = db.execute("SELECT id FROM authors WHERE id=?", (author_id,)).fetchone()
    category = db.execute("SELECT id FROM categories WHERE id=?", (category_id,)).fetchone()

    if not author or not category:
        db.close()
        return jsonify({"error": "Автор або категорія не знайдені"}), 400

    cursor = db.execute("""
        INSERT INTO books (title, author_id, category_id, price, description)
        VALUES (?, ?, ?, ?, ?)
    """, (title, author_id, category_id, price, data.get("description", "")))
    db.commit()
    book_id = cursor.lastrowid
    db.close()

    return jsonify({"message": "Книгу створено", "id": book_id}), 201


@app.route("/api/books/<int:book_id>", methods=["GET", "PUT", "DELETE"])
def api_book_detail(book_id):
    db = get_db()
    book = db.execute("SELECT * FROM books WHERE id=?", (book_id,)).fetchone()

    if not book:
        db.close()
        return jsonify({"error": "Книгу не знайдено"}), 404

    if request.method == "GET":
        result = dict(book)
        db.close()
        return jsonify(result)

    if session.get("role") != "admin":
        db.close()
        return jsonify({"error": "Потрібні права адміністратора"}), 403

    if request.method == "PUT":
        data = request.get_json(silent=True) or {}
        title = str(data.get("title", book["title"])).strip()

        try:
            price = float(data.get("price", book["price"]))
            if not title or price <= 0:
                raise ValueError
        except (ValueError, TypeError):
            db.close()
            return jsonify({"error": "Некоректна назва або ціна"}), 400

        db.execute("""
            UPDATE books SET title=?, price=?, description=? WHERE id=?
        """, (title, price, data.get("description", book["description"]), book_id))
        db.commit()
        db.close()
        return jsonify({"message": "Книгу оновлено"})

    used = db.execute(
        "SELECT id FROM order_items WHERE book_id=? LIMIT 1", (book_id,)
    ).fetchone()

    if used:
        db.close()
        return jsonify({"error": "Книга присутня в замовленнях"}), 409

    db.execute("DELETE FROM books WHERE id=?", (book_id,))
    db.commit()
    db.close()
    return jsonify({"message": "Книгу видалено"})


@app.route("/set-language/<language>")
def set_language(language):
    if language not in ("uk", "en"):
        return "Невідома мова", 400

    response = make_response(redirect(url_for("index")))
    response.set_cookie("language", language, max_age=30 * 24 * 60 * 60, httponly=True, samesite="Lax")
    return response


# PyTest tests

import pytest


@pytest.fixture
def client(tmp_path):
    app.config["TESTING"] = True
    app.config["DATABASE"] = str(tmp_path / "test.db")
    app.config["SECRET_KEY"] = "test-secret"
    init_db()

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Каталог книг" in response.get_data(as_text=True)


def test_api_get_books(client):
    response = client.get("/api/books")
    assert response.status_code == 200
    assert len(response.get_json()) >= 3


def test_register_and_login(client):
    response = client.post("/register", data={
        "username": "testuser",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200

    response = client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert sess["username"] == "testuser"


def test_admin_can_add_book(client):
    client.post("/login", data={
        "username": "admin",
        "password": "admin123"
    })

    response = client.post("/admin/add", data={
        "title": "Тестова книга",
        "author_id": "1",
        "category_id": "1",
        "price": "150",
        "description": "Опис тестової книги"
    })

    assert response.status_code == 302

    response = client.get("/api/books")
    assert any(book["title"] == "Тестова книга" for book in response.get_json())


def test_unknown_book(client):
    response = client.get("/api/books/9999")
    assert response.status_code == 404


if __name__ == "__main__":
    init_db()
    app.run(debug=True)