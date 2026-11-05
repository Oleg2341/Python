
class Student:
    def __init__(self, name, grade, group):
        self.__name = name
        self.grade = grade
        self._group = group

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Ім'я повинно бути рядком")
        if len(value.strip()) < 2:
            raise ValueError("Ім'я повинно містити щонайменше 2 символи")
        self.__name = value

    @property
    def average_grade(self):
        return sum(self.grade) / len(self.grade)

    def show_info(self):
        print("Ім'я:", self.name)
        print("Група:", self._group)
        print("Оцінки:", self.grade)
        print("Середній бал:", round(self.average_grade, 2))


student = Student("Олег", [90, 85, 95, 80], "БІКСб12540")

print("Інформація про студента:")
student.show_info()

print("\nЗміна імені:")
student.name = "Влад"
print("Нове ім'я:", student.name)

print("\nПеревірка некоректних значень:")

try:
    student.name = 123
except TypeError as error:
    print("Помилка:", error)

try:
    student.name = "А"
except ValueError as error:
    print("Помилка:", error)

print("\nСпроба прямого доступу до приватного атрибута:")

try:
    print(student.__name)
except AttributeError as error:
    print("Помилка:", error)

print("\nДоступ через name mangling:")
print(student._Student__name)

print("\nЗміна оцінок:")
student.grade = [100, 90, 95, 85]
print("Нові оцінки:", student.grade)
print("Новий середній бал:", round(student.average_grade, 2))
