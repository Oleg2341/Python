
from flask import Flask, request, make_response, session, redirect, url_for, jsonify


app = Flask(__name__)
app.secret_key = "super-secret-key-for-session"


@app.route("/set-theme/<theme>")
def set_theme(theme):
    response = make_response("Тему встановлено: " + theme)
    response.set_cookie("theme", theme, max_age=30 * 24 * 60 * 60,
                        httponly=True, samesite="Lax")
    return response


@app.route("/get-theme")
def get_theme():
    theme = request.cookies.get("theme", "light")
    return jsonify({"theme": theme})


@app.route("/set-language/<lang>")
def set_language(lang):
    response = make_response("Мову встановлено: " + lang)
    response.set_cookie("language", lang, max_age=30 * 24 * 60 * 60,
                        httponly=True, samesite="Lax")
    return response


@app.route("/preferences")
def preferences():
    return jsonify(dict(request.cookies))


@app.route("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    if product_id not in products_db:
        return jsonify({"error": "Товар не знайдено"}), 404

    cart = session.get("cart", [])
    cart.append(product_id)
    session["cart"] = cart

    return jsonify({
        "message": "Товар додано до кошика",
        "cart": session["cart"]
    })


@app.route("/cart")
def view_cart():
    cart = session.get("cart", [])
    products = []

    for product_id in cart:
        if product_id in products_db:
            products.append({
                "id": product_id,
                "name": products_db[product_id]["name"],
                "price": products_db[product_id]["price"]
            })

    return jsonify({
        "cart": products,
        "total": sum(product["price"] for product in products)
    })


@app.route("/cart/clear")
def clear_cart():
    session.pop("cart", None)
    return jsonify({"message": "Кошик очищено"})


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()

    if not username:
        return jsonify({"error": "Введіть ім'я користувача"}), 400

    session["username"] = username

    return jsonify({"message": "Вхід виконано", "username": username})


@app.route("/logout")
def logout():
    session.pop("username", None)
    return jsonify({"message": "Ви вийшли з акаунта"})


@app.route("/profile")
def profile():
    username = session.get("username")

    if not username:
        return redirect(url_for("login_page"))

    return jsonify({"username": username})


@app.route("/login-page")
def login_page():
    return """
    <form method="POST" action="/login">
        <input type="text" name="username" placeholder="Ваше ім'я">
        <button type="submit">Увійти</button>
    </form>
    """


products_db = {
    1: {"name": "Ноутбук", "price": 25000},
    2: {"name": "Смартфон", "price": 12000},
    3: {"name": "Навушники", "price": 2000},
}


if __name__ == "__main__":
    app.run(debug=True, port=5002)
