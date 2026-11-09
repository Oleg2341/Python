
"""Порівняння ThreadPoolExecutor та ProcessPoolExecutor."""

from concurrent.futures import (
    ThreadPoolExecutor,
    ProcessPoolExecutor,
    as_completed,
)
import time
import hashlib


def io_bound_task(url: str) -> dict:
    """Імітація I/O-bound задачі."""

    time.sleep(0.5)

    return {
        "url": url,
        "status": 200,
        "size": len(url) * 42
    }


def cpu_bound_task(n: int) -> dict:
    """CPU-bound задача: обчислення хеш-суми."""

    hasher = hashlib.sha256()

    for i in range(n):
        hasher.update(str(i).encode())

    return {
        "n": n,
        "hash": hasher.hexdigest()[:16]
    }


def risky_task(value: int) -> float:
    """Задача, що може згенерувати виключення."""

    if value == 0:
        raise ZeroDivisionError("Ділення на нуль!")

    if value < 0:
        raise ValueError("Від'ємне значення: " + str(value))

    return 1000.0 / value


def benchmark_io_bound():
    """Порівняння послідовного та паралельного виконання."""

    urls = [
        "https://api.example.com/data/" + str(i)
        for i in range(20)
    ]

    # Послідовне виконання
    start = time.perf_counter()

    for url in urls:
        io_bound_task(url)

    sequential_time = time.perf_counter() - start

    # Паралельне виконання через ThreadPoolExecutor
    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(io_bound_task, urls))

    parallel_time = time.perf_counter() - start

    print("Кількість завдань:", len(results))
    print("Послідовно:", round(sequential_time, 3), "сек")
    print("Паралельно:", round(parallel_time, 3), "сек")
    print("Прискорення:", round(sequential_time / parallel_time, 2), "x")


def benchmark_cpu_bound():
    """Порівняння послідовного та паралельного виконання."""

    tasks = [500_000] * 8

    # Послідовне виконання
    start = time.perf_counter()

    sequential_results = []

    for n in tasks:
        sequential_results.append(cpu_bound_task(n))

    sequential_time = time.perf_counter() - start

    # Паралельне виконання через ProcessPoolExecutor
    start = time.perf_counter()

    with ProcessPoolExecutor(max_workers=4) as executor:
        parallel_results = list(executor.map(cpu_bound_task, tasks))

    parallel_time = time.perf_counter() - start

    print("Кількість завдань:", len(parallel_results))
    print("Послідовно:", round(sequential_time, 3), "сек")
    print("Паралельно:", round(parallel_time, 3), "сек")
    print("Прискорення:", round(sequential_time / parallel_time, 2), "x")


def handle_exceptions():
    """Демонстрація обробки виключень у пулах."""

    values = [10, 5, 0, -3, 8, 2]

    with ThreadPoolExecutor(max_workers=3) as executor:

        # Створення завдань через submit()
        futures = {}

        for value in values:
            future = executor.submit(risky_task, value)
            futures[future] = value

        # Отримання результатів після завершення завдань
        for future in as_completed(futures):
            value = futures[future]

            try:
                result = future.result()
                print("Число:", value, "| Результат:", result)

            except ZeroDivisionError as error:
                print("Число:", value, "| Помилка:", error)

            except ValueError as error:
                print("Число:", value, "| Помилка:", error)


def main():
    print("=" * 60)
    print("=== I/O-bound: ThreadPoolExecutor ===")
    print("=" * 60)

    benchmark_io_bound()

    print("\n" + "=" * 60)
    print("=== CPU-bound: ProcessPoolExecutor ===")
    print("=" * 60)

    benchmark_cpu_bound()

    print("\n" + "=" * 60)
    print("=== Обробка виключень у пулах ===")
    print("=" * 60)

    handle_exceptions()


if __name__ == "__main__":
    main()
