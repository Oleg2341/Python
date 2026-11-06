"""Типізовані дескриптори та __init_subclass__ для системи конфігурації."""


class ValidatedField:
    """Дескриптор із перевіркою типу та діапазону значень."""

    def __init__(self, expected_type, min_value=None, max_value=None):
        self.expected_type = expected_type
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = "_" + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        if type(value) != self.expected_type:
            raise TypeError("Поле " + self.name + " повинно мати тип " + self.expected_type.__name__)

        if self.min_value is not None and value < self.min_value:
            raise ValueError("Значення поля " + self.name + " менше мінімального")

        if self.max_value is not None and value > self.max_value:
            raise ValueError("Значення поля " + self.name + " більше максимального")

        setattr(obj, self.private_name, value)


class ConfigSection:
    """Базовий клас секції конфігурації."""

    _sections = {}

    def __init_subclass__(cls, section_name="", **kwargs):
        super().__init_subclass__(**kwargs)

        if section_name:
            ConfigSection._sections[section_name] = cls

    @classmethod
    def get_section(cls, name):
        return cls._sections.get(name)

    @classmethod
    def list_sections(cls):
        return list(cls._sections.keys())


class DatabaseConfig(ConfigSection, section_name="database"):
    host = ValidatedField(str)
    port = ValidatedField(int, min_value=1, max_value=65535)
    max_connections = ValidatedField(int, min_value=1, max_value=1000)

    def __init__(self, host, port, max_connections):
        self.host = host
        self.port = port
        self.max_connections = max_connections


class LoggingConfig(ConfigSection, section_name="logging"):
    level = ValidatedField(str)
    max_file_size_mb = ValidatedField(int, min_value=1, max_value=1024)

    def __init__(self, level, max_file_size_mb):
        self.level = level
        self.max_file_size_mb = max_file_size_mb


def main():
    print("Зареєстровані секції:")
    print(ConfigSection.list_sections())

    database = DatabaseConfig("localhost", 5432, 100)

    print("\nНалаштування бази даних:")
    print("Host: " + database.host)
    print("Port: " + str(database.port))
    print("Max connections: " + str(database.max_connections))

    print("\nПеревірка типу:")

    try:
        database.port = "5432"
    except TypeError as error:
        print("Помилка: " + str(error))

    print("\nПеревірка діапазону:")

    try:
        database.port = 70000
    except ValueError as error:
        print("Помилка: " + str(error))

    logging = LoggingConfig("INFO", 100)

    print("\nНалаштування логування:")
    print("Level: " + logging.level)
    print("Max file size: " + str(logging.max_file_size_mb) + " MB")


if __name__ == "__main__":
    main()