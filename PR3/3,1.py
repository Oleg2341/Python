"""Паттерни Singleton та Factory Method."""

from abc import ABC, abstractmethod
from datetime import datetime
import json


class SingletonMeta(type):
    """Метаклас для реалізації патерну Singleton."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in SingletonMeta._instances:
            SingletonMeta._instances[cls] = super().__call__(*args, **kwargs)

        return SingletonMeta._instances[cls]


class LogFormatter(ABC):
    """Абстрактний базовий клас форматера логів."""

    @abstractmethod
    def format(self, level, message, timestamp):
        pass


class PlainFormatter(LogFormatter):
    """Звичайний текстовий формат."""

    def format(self, level, message, timestamp):
        return "[" + level + "] " + timestamp.strftime("%Y-%m-%d %H:%M:%S") + " - " + message


class JSONFormatter(LogFormatter):
    """Форматування у JSON."""

    def format(self, level, message, timestamp):
        data = {
            "level": level,
            "time": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "message": message
        }

        return json.dumps(data, ensure_ascii=False)


class ColorFormatter(LogFormatter):
    """Кольоровий формат для терміналу."""

    COLORS = {
        "DEBUG": "\033[90m",
        "INFO": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m"
    }

    RESET = "\033[0m"

    def format(self, level, message, timestamp):
        color = self.COLORS.get(level, "")
        text = "[" + level + "] " + timestamp.strftime("%Y-%m-%d %H:%M:%S") + " - " + message

        return color + text + self.RESET


class FormatterFactory:
    """Фабрика форматерів."""

    _formatters = {
        "plain": PlainFormatter,
        "json": JSONFormatter,
        "color": ColorFormatter
    }

    @classmethod
    def register(cls, name, formatter_cls):
        if not issubclass(formatter_cls, LogFormatter):
            raise TypeError("Форматер повинен успадковувати LogFormatter")

        cls._formatters[name] = formatter_cls

    @classmethod
    def create(cls, name):
        if name not in cls._formatters:
            raise ValueError("Невідомий форматер: " + name)

        return cls._formatters[name]()

    @classmethod
    def available(cls):
        return list(cls._formatters.keys())


class Logger(metaclass=SingletonMeta):
    """Логер із підтримкою різних рівнів."""

    LEVELS = {
        "DEBUG": 0,
        "INFO": 1,
        "WARNING": 2,
        "ERROR": 3
    }

    def __init__(self, formatter_name="plain", min_level="DEBUG"):
        self._formatter = FormatterFactory.create(formatter_name)
        self._min_level = min_level
        self._log_history = []

    def set_formatter(self, name):
        self._formatter = FormatterFactory.create(name)

    def log(self, level, message):
        if level not in self.LEVELS:
            raise ValueError("Невідомий рівень логування")

        if self._min_level not in self.LEVELS:
            raise ValueError("Невідомий мінімальний рівень логування")

        if self.LEVELS[level] >= self.LEVELS[self._min_level]:
            timestamp = datetime.now()

            result = self._formatter.format(level, message, timestamp)

            print(result)
            self._log_history.append(result)

    def debug(self, msg):
        self.log("DEBUG", msg)

    def info(self, msg):
        self.log("INFO", msg)

    def warning(self, msg):
        self.log("WARNING", msg)

    def error(self, msg):
        self.log("ERROR", msg)

    def get_history(self):
        return self._log_history[:]


def main():
    print("Перевірка Singleton:")

    logger1 = Logger("plain", "DEBUG")
    logger2 = Logger("json", "INFO")

    print("Singleton: " + str(logger1 is logger2))

    print("\nЛогування:")

    logger1.info("Система запущена")
    logger1.warning("Мало пам'яті")
    logger1.error("Помилка з'єднання")

    print("\nЗміна форматера на JSON:")

    logger1.set_formatter("json")
    logger1.debug("Діагностика")

    print("\nЗміна форматера на Color:")

    logger1.set_formatter("color")
    logger1.info("Робота системи продовжується")

    print("\nДоступні форматери:")
    print(FormatterFactory.available())

    print("\nІсторія логів:")
    print("Кількість записів: " + str(len(logger1.get_history())))

    for record in logger1.get_history():
        print(record)


if __name__ == "__main__":
    main()