import itertools


def arithmetic_progression(start, step):
    while True:
        yield start
        start += step


def geometric_progression(start, ratio, limit=float("inf")):
    while start <= limit:
        yield start
        start *= ratio


def fibonacci(n=None):
    a = 0
    b = 1
    count = 0

    while n is None or count < n:
        yield a
        a, b = b, a + b
        count += 1


def collatz_sequence(n):
    while n != 1:
        yield n

        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1

    yield 1


def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def main():
    ap = arithmetic_progression(2, 3)
    first_10 = list(itertools.islice(ap, 10))
    print("Арифметична прогресія: " + str(first_10))

    gp = list(geometric_progression(1, 2, limit=1000))
    print("Геометрична прогресія: " + str(gp))

    fib_15 = list(fibonacci(15))
    print("Числа Фібоначчі: " + str(fib_15))

    coll = list(collatz_sequence(27))
    print("Коллатц: довжина = " + str(len(coll)) + ", максимум = " + str(max(coll)))

    nested = [1, [2, 3], [4, [5, 6]], 7, [8, [9, [10]]]]
    flat = list(flatten(nested))
    print("Розгортання списку: " + str(flat))

    for fib_num in fibonacci(None):
        if fib_num > 10000:
            print("Перше число Фібоначчі більше 10000: " + str(fib_num))
            break


if __name__ == "__main__":
    main()