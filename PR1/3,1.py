def factorial(n: int) -> int:
    result = 1

    for i in range(1, n + 1):
        result = result * i

    return result


def harmonic_sum(n: int) -> float:
    result = 0

    for i in range(1, n + 1):
        result = result + 1 / i

    return result


def multiplication_table(n: int) -> None:
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            print("" + str(i * j).rjust(4), end="")
        print()


def main():
    n = int(input("Введіть число n: "))

    print("" + str(n) + "! = " + str(factorial(n)))
    print("Гармонічна сума H(" + str(n) + ") = " + str(round(harmonic_sum(n), 6)))

    print("\nТаблиця множення " + str(n) + "x" + str(n) + ":")
    multiplication_table(n)


if __name__ == "__main__":
    main()