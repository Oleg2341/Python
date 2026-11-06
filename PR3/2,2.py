"""Декоратори класів."""

import functools
import time


def auto_repr(cls):
    """Декоратор, який автоматично додає __repr__."""

    parameters = cls.__init__.__code__.co_varnames[1:cls.__init__.__code__.co_argcount]

    def __repr__(self):
        values = []

        for name in parameters:
            values.append(name + "=" + repr(getattr(self, name)))

        return cls.__name__ + "(" + ", ".join(values) + ")"

    cls.__repr__ = __repr__

    return cls


def frozen(cls):
    """Декоратор, який забороняє змінювати атрибути після створення об'єкта."""

    original_init = cls.__init__

    @functools.wraps(original_init)
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        object.__setattr__(self, "_frozen", True)

    def new_setattr(self, name, value):
        if getattr(self, "_frozen", False):
            raise AttributeError("Не можна змінювати атрибути об'єкта")

        object.__setattr__(self, name, value)

    cls.__init__ = new_init
    cls.__setattr__ = new_setattr

    return cls


def log_methods(cls):
    """Декоратор, який логує виклики публічних методів."""

    for name, method in list(cls.__dict__.items()):
        if callable(method) and not name.startswith("_"):

            @functools.wraps(method)
            def wrapper(self, *args, _method=method, _name=name, **kwargs):
                print("[LOG] Виклик методу " + _name)

                start_time = time.time()

                try:
                    result = _method(self, *args, **kwargs)

                    end_time = time.time()

                    print("[LOG] Результат: " + str(result))
                    print("[LOG] Час виконання: " +
                          str(round(end_time - start_time, 4)) + "с")

                    return result

                except Exception as error:
                    print("[ERROR] " + str(error))
                    raise

            setattr(cls, name, wrapper)

    return cls


@auto_repr
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


@frozen
class ImmutableConfig:
    def __init__(self, host: str, port: int, debug: bool = False):
        self.host = host
        self.port = port
        self.debug = debug


@log_methods
class MathService:
    def add(self, a: float, b: float) -> float:
        return a + b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Ділення на нуль")

        return a / b


def main():
    print("Перевірка auto_repr:")

    p = Point(3.0, 4.0)
    print(repr(p))

    print("\nПеревірка frozen:")

    cfg = ImmutableConfig("localhost", 8080, debug=True)

    print("Config: " + cfg.host + ":" + str(cfg.port))

    try:
        cfg.host = "remote"
    except AttributeError as e:
        print("Очікувана помилка: " + str(e))

    print("\nПеревірка log_methods:")

    svc = MathService()

    svc.add(10, 20)
    svc.multiply(3, 7)

    try:
        svc.divide(10, 0)
    except ValueError as e:
        print("Помилка: " + str(e))


if __name__ == "__main__":
    main()