
from flask import Flask, request, jsonify
from datetime import datetime


app = Flask(__name__)


students_db = {}
next_id = 1


@app.route("/api/students", methods=["GET"])
def get_students():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    group = request.args.get("group")
    min_gpa = request.args.get("min_gpa", type=float)
    sort_by = request.args.get("sort_by", "name")
    order = request.args.get("order", "asc")

    if page < 1 or per_page < 1:
        return jsonify({"error": "Некоректна пагінація"}), 400

    students = list(students_db.values())

    if group:
        students = [s for s in students if s["group"] == group]

    if min_gpa is not None:
        students = [s for s in students if s["gpa"] >= min_gpa]

    if sort_by not in ["name", "gpa", "group"]:
        return jsonify({"error": "Некоректне поле сортування"}), 400

    if order not in ["asc", "desc"]:
        return jsonify({"error": "Некоректний порядок сортування"}), 400

    students.sort(key=lambda s: s[sort_by], reverse=(order == "desc"))

    count = len(students)
    start = (page - 1) * per_page
    students = students[start:start + per_page]

    return jsonify({
        "count": count,
        "page": page,
        "per_page": per_page,
        "students": students
    }), 200


@app.route("/api/students", methods=["POST"])
def create_student():
    global next_id

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Очікується JSON"}), 400

    name = str(data.get("name", "")).strip()
    group = str(data.get("group", "")).strip()
    email = str(data.get("email", "")).strip()
    
    if not name or not group:
        return jsonify({"error": "Ім'я та група обов'язкові"}), 400

    try:
        gpa = float(data.get("gpa"))
    except (ValueError, TypeError):
        return jsonify({"error": "Середній бал повинен бути числом"}), 400

    if not 0 <= gpa <= 100:
        return jsonify({"error": "Середній бал має бути від 0 до 100"}), 400

    if email:
        for student in students_db.values():
            if student["email"] == email:
                return jsonify({"error": "Такий email вже існує"}), 400

    student = {
        "id": next_id,
        "name": name,
        "group": group,
        "email": email,
        "gpa": gpa,
        "created_at": datetime.now().isoformat()
    }

    students_db[next_id] = student
    next_id += 1

    return jsonify(student), 201


@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = students_db.get(student_id)

    if student is None:
        return jsonify({"error": "Студента не знайдено"}), 404

    return jsonify(student), 200


@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    student = students_db.get(student_id)

    if student is None:
        return jsonify({"error": "Студента не знайдено"}), 404

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Очікується JSON"}), 400

    name = str(data.get("name", "")).strip()
    group = str(data.get("group", "")).strip()
    email = str(data.get("email", "")).strip()

    if not name or not group:
        return jsonify({"error": "Ім'я та група обов'язкові"}), 400

    try:
        gpa = float(data.get("gpa"))
    except (ValueError, TypeError):
        return jsonify({"error": "Середній бал повинен бути числом"}), 400

    if not 0 <= gpa <= 100:
        return jsonify({"error": "Середній бал має бути від 0 до 100"}), 400

    for other_id, other in students_db.items():
        if other_id != student_id and email and other["email"] == email:
            return jsonify({"error": "Такий email вже існує"}), 400

    student["name"] = name
    student["group"] = group
    student["email"] = email
    student["gpa"] = gpa

    return jsonify(student), 200


@app.route("/api/students/<int:student_id>", methods=["PATCH"])
def patch_student(student_id):
    student = students_db.get(student_id)

    if student is None:
        return jsonify({"error": "Студента не знайдено"}), 404

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Очікується JSON"}), 400

    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            return jsonify({"error": "Некоректне ім'я"}), 400
        student["name"] = data["name"].strip()

    if "group" in data:
        if not isinstance(data["group"], str) or not data["group"].strip():
            return jsonify({"error": "Некоректна група"}), 400
        student["group"] = data["group"].strip()

    if "email" in data:
        email = str(data["email"]).strip()

        for other_id, other in students_db.items():
            if other_id != student_id and email and other["email"] == email:
                return jsonify({"error": "Такий email вже існує"}), 400

        student["email"] = email

    if "gpa" in data:
        try:
            gpa = float(data["gpa"])
        except (ValueError, TypeError):
            return jsonify({"error": "Некоректний середній бал"}), 400

        if not 0 <= gpa <= 100:
            return jsonify({"error": "Бал має бути від 0 до 100"}), 400

        student["gpa"] = gpa

    return jsonify(student), 200


@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    if student_id not in students_db:
        return jsonify({"error": "Студента не знайдено"}), 404

    del students_db[student_id]

    return "", 204


@app.route("/api/students/stats", methods=["GET"])
def students_stats():
    students = list(students_db.values())

    total = len(students)

    if total > 0:
        avg_gpa = round(sum(s["gpa"] for s in students) / total, 2)
    else:
        avg_gpa = 0

    groups = {}

    for student in students:
        group = student["group"]
        groups[group] = groups.get(group, 0) + 1

    top_students = sorted(
        students,
        key=lambda s: s["gpa"],
        reverse=True
    )[:3]

    return jsonify({
        "total": total,
        "avg_gpa": avg_gpa,
        "groups": groups,
        "top_students": top_students
    }), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ресурс не знайдено", "status": 404}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Некоректний запит", "status": 400}), 400


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"error": "Помилка валідації", "status": 422}), 422


if __name__ == "__main__":
    test_students = [
        {"name": "Іваненко О.", "group": "КІ-21", "email": "ivan@kpi.ua", "gpa": 85.5},
        {"name": "Петренко М.", "group": "КІ-21", "email": "petro@kpi.ua", "gpa": 92.0},
        {"name": "Сидоренко А.", "group": "КІ-22", "email": "syd@kpi.ua", "gpa": 78.3},
        {"name": "Коваль Л.", "group": "КІ-22", "email": "koval@kpi.ua", "gpa": 95.1},
    ]

    for s in test_students:
        students_db[next_id] = {
            **s,
            "id": next_id,
            "created_at": datetime.now().isoformat()
        }
        next_id += 1

    app.run(debug=True, port=5005)
