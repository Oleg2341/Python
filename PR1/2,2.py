import math


def triangle_type(a, b, c):
    if a <= 0 or b <= 0 or c <= 0:
        return "не є трикутником"

    if a + b <= c or a + c <= b or b + c <= a:
        return "не є трикутником"

    if a == b and b == c:
        return "рівносторонній"

    elif a == b or a == c or b == c:
        return "рівнобедрений"

    else:
        sides = sorted([a, b, c])

        if math.isclose(sides[0] ** 2 + sides[1] ** 2, sides[2] ** 2, abs_tol=1e-9):
            return "прямокутний"
        else:
            return "різносторонній"


def triangle_area(a, b, c):
    p = (a + b + c) / 2
    area = math.sqrt(p * (p - a) * (p - b) * (p - c))
    return area


def main():
    a = float(input("Введіть сторону A: "))
    b = float(input("Введіть сторону B: "))
    c = float(input("Введіть сторону C: "))

    result = triangle_type(a, b, c)

    print("Сторона A: " + str(a))
    print("Сторона B: " + str(b))
    print("Сторона C: " + str(c))
    print("Тип трикутника: " + result)

    if result != "не є трикутником":
        area = triangle_area(a, b, c)
        print("Площа трикутника: " + str(round(area, 2)))
    else:
        print("Площа трикутника: неможливо обчислити")


if __name__ == "__main__":
    main()