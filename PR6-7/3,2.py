
from flask import Flask, request, jsonify, g
from datetime import datetime
from functools import wraps


app = Flask(__name__)


class StudentSerializer:

    @staticmethod
    def serialize(student: dict, fields: list = None) -> dict:
        result = dict(student)

        if "created_at" in result:
            result["created_at"] = str(result["created_at"])

        result["gpa_status"] = "Відмінно" if result["gpa"] >= 90 else "Добре" if result["gpa"] >= 75 else "Задовільно"

        if fields:
            result = {key: result[key] for key in fields if key in result}

        return result

    @staticmethod
    def deserialize(data: dict) -> dict:
        errors = {}

        required_fields = ["name", "group", "email", "gpa"]

        for field in required_fields:
            if field not in data or data[field] == "":
                errors[field] = "Поле обов'язкове"

        if errors:
            raise APIError("Помилка валідації", 422, errors)

        try:
            gpa = float(data["gpa"])
        except (ValueError, TypeError):
            raise APIError("Середній бал повинен бути числом", 422)

        if not 0 <= gpa <= 100:
            raise APIError("Середній бал повинен бути від 0 до 100", 422)

        return {
            "name": str(data["name"]).strip(),
            "group": str(data["group"]).strip(),
            "email": str(data["email"]).strip(),
            "gpa": gpa
        }

    @staticmethod
    def serialize_list(students: list, fields: list = None) -> list:
        return [StudentSerializer.serialize(s, fields) for s in students]


@app.before_request
def log_request():
    g.request_time = datetime.now()
    print("Метод:", request.method)
    print("URL:", request.url)
    print("Час:", g.request_time)


@app.after_request
def add_headers(response):
    if hasattr(g, "request_time"):
        response.headers["X-Request-Time"] = str(g.request_time)

    response.headers["Access-Control-Allow-Origin"] = "*"

    return response


def require_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")

        if api_key != "secret-api-key-123":
            return jsonify({"error": "Невірний API-ключ"}), 401

        return f(*args, **kwargs)

    return wrapper


students_db = {}
next_id = 1


@app.route("/api/v2/students", methods=["GET"])
def get_students_v2():
    students = list(students_db.values())

    search = request.args.get("search", "").lower()
    sort = request.args.get("sort", "name")
    order = request.args.get("order", "asc")
    fields = request.args.get("fields")

    if search:
        students = [
            s for s in students
            if search in s["name"].lower()
            or search in s["group"].lower()
            or search in s["email"].lower()
        ]

    if sort not in ["name", "group", "gpa"]:
        raise APIError("Некоректне поле сортування", 400)

    if order not in ["asc", "desc"]:
        raise APIError("Некоректний порядок сортування", 400)

    students.sort(
        key=lambda s: s[sort],
        reverse=(order == "desc")
    )

    if fields:
        fields = [field.strip() for field in fields.split(",")]

    result = StudentSerializer.serialize_list(students, fields)

    return jsonify({
        "count": len(result),
        "students": result
    }), 200


@app.route("/api/v2/students", methods=["POST"])
@require_api_key
def create_student_v2():
    global next_id

    data = request.get_json(silent=True)

    if data is None:
        raise APIError("Очікується JSON", 400)

    student_data = StudentSerializer.deserialize(data)

    for student in students_db.values():
        if student["email"] == student_data["email"]:
            raise APIError("Такий email вже існує", 400)

    student = {
        "id": next_id,
        **student_data,
        "created_at": datetime.now().isoformat()
    }

    students_db[next_id] = student
    next_id += 1

    return jsonify(StudentSerializer.serialize(student)), 201


class APIError(Exception):

    def __init__(self, message: str, status_code: int = 400, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}


@app.errorhandler(APIError)
def handle_api_error(error):
    response = {
        "error": error.message,
        "status": error.status_code,
        "details": error.details,
        "timestamp": datetime.now().isoformat()
    }

    return jsonify(response), error.status_code


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Ресурс не знайдено",
        "status": 404
    }), 404


if __name__ == "__main__":
    app.run(debug=True, port=5006)
