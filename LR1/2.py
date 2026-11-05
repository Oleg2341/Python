
students = [
    ("Рудиченко", "БІКСб-12540", [85, 90, 78]),
    ("Черемухім", "БІКСб-12540", [92, 88, 95]),
    ("Кульбачук", "БІКСб-12540", [76, 81, 89])
]

def abc(student):
    surname, group, bal = student
    print("Прізвище:", surname)
    print("Група:", group)
    print("Оцінки:", bal)

def average(students):
    total = 0
    count = 0

    for student in students:
        for grade in student[2]:
            total += grade
            count += 1

    return total / count

print("Список студентів:")

for student in students:
    abc(student)
    print()

print("Середній бал усіх студентів:", round(average(students), 2))

print("Спроба змінити кортеж:")

try:
    students[0][0] = "Сидоренко"
except TypeError:
    print("Помилка: кортеж не можна змінювати")

print("Кортеж зі списком оцінок:")

student = students[0]
print("До зміни:", student)

student[2].append(95)

print("Після зміни:", student)
