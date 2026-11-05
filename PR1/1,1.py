import math

def main():
    a = float(input("Введіть a: "))
    b = float(input("Введіть b: "))
    c = float(input("Введіть c: "))

    sum_squares = a**2 + b**2 + c**2
    average = (a + b + c) / 3
    discriminant = b**2 - 4 * a * c
    hypotenuse = math.sqrt(a**2 + b**2)

    is_triangle = (a + b > c) and (a + c > b) and (b + c > a) and (a > 0 or b > 0 or c > 0)

    print("Сума квадратів: " + str(round(sum_squares, 2)))
    print("Середнє арифметичне: " + str(round(average, 2)))
    print("Дискримінант: " + str(round(discriminant, 2)))
    print("Гіпотенуза: " + str(round(hypotenuse, 2)))
    print("Чи утворюють трикутник: " + str(is_triangle))

if __name__ == "__main__":
    main()