"""Система плагінів з автоматичною реєстрацією через метаклас."""

from abc import abstractmethod


class PluginMeta(type):

    _registry: dict[str, type] = {}
    REQUIRED_ATTRS = ("name", "version")

    def __new__(mcs, cls_name: str, bases: tuple, namespace: dict):
        cls = super().__new__(mcs, cls_name, bases, namespace)

        if bases:
            for attr in mcs.REQUIRED_ATTRS:
                if attr not in namespace:
                    raise TypeError("Клас " + cls_name + " не має обов'язкового атрибута " + attr)

            mcs._registry[namespace["name"]] = cls

        return cls

    @classmethod
    def get_registry(mcs) -> dict[str, type]:
        return mcs._registry.copy()

    @classmethod
    def create_plugin(mcs, plugin_name: str):
        if plugin_name not in mcs._registry:
            raise ValueError("Плагін " + plugin_name + " не знайдено")

        return mcs._registry[plugin_name]()


class BasePlugin(metaclass=PluginMeta):

    @abstractmethod
    def execute(self, data: str) -> str:
        """Обробити вхідні дані."""
        pass


class UpperPlugin(BasePlugin):
    name = "upper"
    version = "1.0"

    def execute(self, data: str) -> str:
        return data.upper()


class ReversePlugin(BasePlugin):
    name = "reverse"
    version = "1.0"

    def execute(self, data: str) -> str:
        return data[::-1]


class CensorPlugin(BasePlugin):
    name = "censor"
    version = "1.1"

    def execute(self, data: str) -> str:
        words = ["погано", "помилка", "тест"]

        for word in words:
            data = data.replace(word, "***")

        return data


HashPlugin = type(
    "HashPlugin",
    (BasePlugin,),
    {
        "name": "hash",
        "version": "2.0",
        "execute": lambda self, data: str(hash(data))
    }
)


def main():

    print("Зареєстровані плагіни:")

    for name, cls in PluginMeta.get_registry().items():
        print("  " + name + " (v" + cls.version + "): " + cls.__name__)

    print("\nРезультати роботи плагінів:")

    test_data = "Привіт Світ"

    for name in PluginMeta.get_registry():
        plugin = PluginMeta.create_plugin(name)
        print("  " + name + ": " + plugin.execute(test_data))

    print("\nПеревірка помилки:")

    try:
        class WrongPlugin(BasePlugin):
            def execute(self, data: str) -> str:
                return data

    except TypeError as e:
        print("  Помилка:", e)


if __name__ == "__main__":
    main()