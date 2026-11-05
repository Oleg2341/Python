
class Purchase:
    def __enter__(self):
        print("Початок оформлення покупки.")
        return self

    def __exit__(self, type, value, traceback):
        print("Оформлення покупки завершено.")


def scene1():
    print("\n--- Завдання 1. Перевірка суми покупки ---")

    try:
        price = float(input("Введіть суму покупки: "))

        if price < 0:
            raise ValueError

        print("Сума покупки: " + str(price) + " грн")

    except ValueError:
        print("Помилка! Введіть правильну суму.")


def scene2():
    print("\n--- Завдання 2. Розрахунок знижки ---")

    try:
        price = float(input("Введіть суму покупки: "))
        discount = float(input("Введіть знижку у відсотках: "))

        if price < 0 or discount < 0 or discount > 100:
            raise ValueError

        total = price - (price * discount / 100)

    except ValueError:
        print("Помилка! Перевірте введені числа.")

    else:
        print("Сума зі знижкою: " + str(round(total, 2)) + " грн")

    finally:
        print("Розрахунок завершено.")


def scene3():
    print("\n--- Завдання 3. Оформлення покупки ---")

    try:
        with Purchase() as purchase:
            price = float(input("Введіть ціну товару: "))
            count = int(input("Введіть кількість товару: "))

            if price < 0 or count < 0:
                raise ValueError

            if count == 0:
                raise ZeroDivisionError

            total = price * count

            print("Загальна вартість: " + str(total) + " грн")

    except (ValueError, ZeroDivisionError):
        print("Помилка! Перевірте ціну та кількість товару.")


scene1()
scene2()
scene3()
