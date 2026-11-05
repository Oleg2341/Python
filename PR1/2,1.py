def classify_grade(score: int) -> str:
    if score >= 90:
        return "A"
    elif score >= 82:
        return "B"
    elif score >= 74:
        return "C"
    elif score >= 64:
        return "D"
    elif score >= 60:
        return "E"
    elif score >= 35:
        return "FX"
    else:
        return "F"


def main():
    raw = input("Введіть оцінку (0-100): ")

    try:
        score = int(raw)

        if score < 0 or score > 100:
            print("Помилка: оцінка має бути від 0 до 100")
        else:
            grade = classify_grade(score)
            print("Оцінка ЄКТС: "+ grade)

            passed = grade not in ("FX", "F")

            if passed:
                print("Результат: Зараховано")
            else:
                print("Результат: Не зараховано")

    except ValueError:
        print("Помилка: потрібно ввести ціле число")


if __name__ == "__main__":
    main()