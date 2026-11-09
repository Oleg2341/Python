
"""Паралельне обчислення з multiprocessing."""

import multiprocessing
import time
import os


def is_prime(n: int) -> bool:
    """Перевірка числа на простоту."""

    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5

    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True


def sum_primes_in_range(start: int, end: int) -> tuple[int, int, int]:
    """Обчислює суму та кількість простих чисел у діапазоні."""

    pid = os.getpid()
    total_sum = 0
    count = 0

    for number in range(start, end):
        if is_prime(number):
            total_sum += number
            count += 1

    return total_sum, count, pid


def main():
    total_range = 1_000_000
    num_workers = 4

    # Розбиття діапазону на частини
    chunk_size = (total_range - 2) // num_workers
    ranges = []

    for i in range(num_workers):
        start = 2 + i * chunk_size

        if i == num_workers - 1:
            end = total_range
        else:
            end = start + chunk_size

        ranges.append((start, end))

    # Послідовне виконання
    start_time = time.perf_counter()

    sequential_results = []

    for start, end in ranges:
        result = sum_primes_in_range(start, end)
        sequential_results.append(result)

    seq_time = time.perf_counter() - start_time

    seq_sum = sum(result[0] for result in sequential_results)
    seq_count = sum(result[1] for result in sequential_results)

    # Паралельне виконання
    start_time = time.perf_counter()

    with multiprocessing.Pool(processes=num_workers) as pool:
        parallel_results = pool.starmap(sum_primes_in_range, ranges)

    par_time = time.perf_counter() - start_time

    par_sum = sum(result[0] for result in parallel_results)
    par_count = sum(result[1] for result in parallel_results)

    # Виведення результатів
    print("Послідовне виконання:")
    print("Сума простих чисел:", seq_sum)
    print("Кількість простих чисел:", seq_count)

    print("\nПаралельне виконання:")

    for i, result in enumerate(parallel_results):
        print("Процес", i + 1, "| PID:", result[2])
        print("Сума:", result[0], "| Кількість:", result[1])

    print("\nЗагальна сума:", par_sum)
    print("Загальна кількість:", par_count)

    print("\nПослідовно: " + str(round(seq_time, 3)) + " сек")
    print("Паралельно (" + str(num_workers) + " процеси): " + str(round(par_time, 3)) + " сек")

    if par_time > 0:
        print("Прискорення: " + str(round(seq_time / par_time, 2)) + "x")


if __name__ == "__main__":
    main()
