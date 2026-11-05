
def main():
    raw_input = input("Введіть число: ")

    try:
        number_int = int(raw_input)
        number_float = float(raw_input)
        number_bool = bool(raw_input)

        print("Ціле число: " + str(number_int))
        print("Дробове число: " + str(round(number_float, 2)))
        print("Булеве значення: " + str(number_bool))

        print("Тип int: " + str(type(number_int)))
        print("Тип float: " + str(type(number_float)))
        print("Тип bool: " + str(type(number_bool)))

    except ValueError:
        print("Помилка! Ви ввели не число.")

    name = input("Введіть ім'я: ")
    age = int(input("Введіть вік: "))

    print("Ім'я: " + str(name))
    print("Вік: " + str(age))
    print(f"Ім'я: {name:<15}")
    print(f"Вік: {age:03d}")
    print(f"Вік через рік: {age + 1:.2f}")

    numbers = list(range(1, 6))

    print("Список чисел: " + str(numbers))
    print("Кількість елементів: " + str(len(numbers)))
    print("ID списку: " + str(id(numbers)))

if __name__ == "__main__":
    main()
