from collections import namedtuple


Student = namedtuple("Student", ["name", "grade"])


class StudentGroupIterator:
    def __init__(self, students):
        self._students = students
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._students):
            raise StopIteration

        student = self._students[self._index]
        self._index += 1

        return student


class StudentGroup:
    def __init__(self, group_name):
        self._group_name = group_name
        self._students = []

    def add_student(self, name, grade):
        self._students.append(Student(name, grade))

    def __iter__(self):
        return StudentGroupIterator(self._students)

    def __len__(self):
        return len(self._students)

    def top_students(self, n=3):
        students = sorted(self._students, key=lambda student: student.grade, reverse=True)
        return iter(students[:n])


def main():
    group = StudentGroup("БІКСб12540")

    group.add_student("Олег", 95)
    group.add_student("Макс", 78)
    group.add_student("Даня", 92)
    group.add_student("Денис", 85)
    group.add_student("Ілля", 88)

    print("Перший обхід:")
    for student in group:
        print(student.name + ": " + str(student.grade))

    print("\nДругий обхід:")
    for student in group:
        print(student.name + ": " + str(student.grade))

    print("\nВсі пари студентів:")
    for s1 in group:
        for s2 in group:
            if s1.name < s2.name:
                print(s1.name + " та " + s2.name)

    print("\nТоп-3 студенти:")
    for student in group.top_students(3):
        print(student.name + ": " + str(student.grade))


if __name__ == "__main__":
    main()