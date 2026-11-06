"""Декоратори функцій з параметрами."""

import functools
import time


def cache(max_size=128):
    """Декоратор кешування результатів функції."""

    def decorator(func):
        _cache = {}
        _call_order = []

        @functools.wraps(func)
        def wrapper(*args):
            if args in _cache:
                print("cache hit")
                return _cache[args]

            print("cache miss")
            result = func(*args)

            _cache[args] = result
            _call_order.append(args)

            if len(_cache) > max_size:
                old_args = _call_order.pop(0)
                del _cache[old_args]

            return result

        wrapper.cache_info = lambda: {
            "size": len(_cache),
            "max_size": max_size
        }

        wrapper.cache_clear = lambda: (_cache.clear(), _call_order.clear())

        return wrapper

    return decorator


def rate_limit(max_calls, period=60.0):
    """Декоратор обмеження кількості викликів."""

    def decorator(func):
        call_times = []

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()

            while call_times and current_time - call_times[0] > period:
                call_times.pop(0)

            if len(call_times) >= max_calls:
                raise RuntimeError("Перевищено ліміт викликів функції")

            call_times.append(current_time)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def log(level="INFO"):
    """Декоратор логування функції."""

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print("[" + level + "] Виклик " + func.__name__ +
                  str(args) + str(kwargs))

            start_time = time.time()

            try:
                result = func(*args, **kwargs)

                end_time = time.time()
                execution_time = end_time - start_time

                print("[" + level + "] " + func.__name__ +
                      " -> " + str(result) +
                      " (час: " + str(round(execution_time, 4)) + "с)")

                return result

            except Exception as error:
                print("[ERROR] " + str(error))
                raise

        return wrapper

    return decorator


@cache(max_size=64)
def fibonacci(n: int) -> int:
    """Обчислює n-е число Фібоначчі рекурсивно."""

    if n < 2:
        return n

    return fibonacci(n - 1) + fibonacci(n - 2)


@rate_limit(max_calls=5, period=10.0)
def send_notification(message: str) -> str:
    """Імітує відправку сповіщення."""

    return "Надіслано: " + message


@log(level="DEBUG")
def divide(a: float, b: float) -> float:
    """Ділення з можливим ZeroDivisionError."""

    return a / b


def main():
    print("Обчислення числа Фібоначчі:")

    result = fibonacci(30)
    print("Результат: " + str(result))

    print("Інформація про кеш:")
    print(fibonacci.cache_info())

    print("\nВідправка сповіщень:")

    for i in range(6):
        try:
            result = send_notification("Повідомлення " + str(i + 1))
            print(result)
        except RuntimeError as error:
            print("Помилка: " + str(error))

    print("\nПеревірка ділення:")

    try:
        result = divide(10, 3)
        print("Результат ділення: " + str(result))
    except ZeroDivisionError as error:
        print("Помилка: " + str(error))

    try:
        result = divide(10, 0)
        print("Результат ділення: " + str(result))
    except ZeroDivisionError as error:
        print("Помилка: " + str(error))


if __name__ == "__main__":
    main()