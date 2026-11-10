
from flask import Flask, request, jsonify, abort
from functools import wraps


app = Flask(__name__)


def validate_json(required_fields):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json(silent=True)

            if data is None:
                return jsonify({"error": "Очікується JSON"}), 400

            missing = [field for field in required_fields if field not in data]

            if missing:
                return jsonify({
                    "error": "Відсутні поля: " + ", ".join(missing)
                }), 400

            return f(*args, **kwargs)

        return wrapper
    return decorator


items_db = {
    1: {"id": 1, "name": "Ноутбук", "price": 25000, "category": "електроніка"},
    2: {"id": 2, "name": "Книга Python", "price": 500, "category": "книги"},
    3: {"id": 3, "name": "Навушники", "price": 2000, "category": "електроніка"},
}

next_id = 4


@app.route("/api/items", methods=["GET"])
def get_items():
    category = request.args.get("category")
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    sort = request.args.get("sort", "name")
    order = request.args.get("order", "asc")

    items = list(items_db.values())

    if category:
        items = [item for item in items if item["category"] == category]

    if min_price is not None:
        items = [item for item in items if item["price"] >= min_price]

    if max_price is not None:
        items = [item for item in items if item["price"] <= max_price]

    if sort not in ["name", "price"]:
        return jsonify({"error": "Некоректне поле сортування"}), 400

    if order not in ["asc", "desc"]:
        return jsonify({"error": "Некоректний напрямок сортування"}), 400

    items.sort(key=lambda item: item[sort], reverse=(order == "desc"))

    return jsonify({
        "items": items,
        "total": len(items),
        "sort": sort,
        "order": order
    }), 200


@app.route("/api/items", methods=["POST"])
@validate_json(["name", "price", "category"])
def create_item():
    global next_id

    data = request.get_json()

    name = str(data["name"]).strip()
    category = str(data["category"]).strip()

    try:
        price = float(data["price"])
    except (ValueError, TypeError):
        return jsonify({"error": "Ціна повинна бути числом"}), 400

    if not name:
        return jsonify({"error": "Назва не може бути порожньою"}), 400

    if not category:
        return jsonify({"error": "Категорія не може бути порожньою"}), 400

    if price <= 0:
        return jsonify({"error": "Ціна повинна бути більшою за 0"}), 400

    item = {
        "id": next_id,
        "name": name,
        "price": price,
        "category": category
    }

    items_db[next_id] = item
    next_id += 1

    return jsonify(item), 201


@app.route("/api/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = items_db.get(item_id)

    if item is None:
        abort(404)

    return jsonify(item), 200


@app.route("/api/items/<int:item_id>", methods=["PUT"])
@validate_json(["name", "price", "category"])
def update_item(item_id):
    item = items_db.get(item_id)

    if item is None:
        abort(404)

    data = request.get_json()

    name = str(data["name"]).strip()
    category = str(data["category"]).strip()

    try:
        price = float(data["price"])
    except (ValueError, TypeError):
        return jsonify({"error": "Ціна повинна бути числом"}), 400

    if not name or not category:
        return jsonify({"error": "Назва та категорія не можуть бути порожніми"}), 400

    if price <= 0:
        return jsonify({"error": "Ціна повинна бути більшою за 0"}), 400

    item["name"] = name
    item["price"] = price
    item["category"] = category

    return jsonify(item), 200


@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    if item_id not in items_db:
        abort(404)

    del items_db[item_id]

    return "", 204


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ресурс не знайдено"}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Некоректний запит"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5001)
