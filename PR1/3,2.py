def calculator():
    print("=== Калькулятор ===")
    print("Введіть вираз у форматі: число оператор число")
    print("Введіть 'quit' для виходу, 'history' для історії")

    history = []

    while True:
        user_input = input("\n> ").strip()

        if user_input == "quit":
            print("Калькулятор завершено")
            break

        if user_input == "history":
            if len(history) == 0:
                print("Історія порожня")
            else:
                for item in history:
                    print(item)
            continue

        parts = user_input.split()

        if len(parts) != 3:
            print("Помилка! Введіть правильний вираз")
            continue

        try:
            a = float(parts[0])
            operator = parts[1]
            b = float(parts[2])
        except ValueError:
            print("Помилка! Введіть числа")
            continue

        if operator == "+":
            result = a + b
        elif operator == "-":
            result = a - b
        elif operator == "*":
            result = a * b
        elif operator == "/":
            if b == 0:
                print("Помилка! Ділення на нуль")
                continue
            result = a / b
        elif operator == "//":
            if b == 0:
                print("Помилка! Ділення на нуль")
                continue
            result = a // b
        elif operator == "%":
            if b == 0:
                print("Помилка! Ділення на нуль")
                continue
            result = a % b
        elif operator == "**":
            result = a ** b
        else:
            print("Невідомий оператор")
            continue

        print("Результат: " + str(result))

        history.append(str(a) + " " + operator + " " + str(b) + " = " + str(result))


if __name__ == "__main__":
    calculator()