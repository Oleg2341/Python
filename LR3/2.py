
class ShopError(Exception):
    pass


class ValidationError(ShopError):
    def __init__(self, field, code):
        self.field = field
        self.code = code

    def __str__(self):
        return "Помилка перевірки поля " + self.field + ". Код: " + self.code


class ProductNotFoundError(ShopError):
    def __init__(self, product_id):
        self.product_id = product_id

    def __str__(self):
        return "Товар з номером " + self.product_id + " не знайдено."


class InsufficientStockError(ShopError):
    def __init__(self, product_id, available):
        self.product_id = product_id
        self.available = available

    def __str__(self):
        return "Недостатньо товару на складі. Доступно: " + str(self.available)


products = {
    "P001": {"name": "Ноутбук", "stock": 5},
    "P002": {"name": "Мишка", "stock": 10},
    "P003": {"name": "Клавіатура", "stock": 7}
}


def check_quantity(quantity):
    if quantity <= 0:
        raise ValidationError("кількість", "E001")

    return quantity


def find_product(product_id):
    try:
        product = products[product_id]
        return product

    except KeyError as error:
        raise ProductNotFoundError(product_id) from error


def buy_product(product_id, quantity):
    check_quantity(quantity)

    product = find_product(product_id)

    if quantity > product["stock"]:
        raise InsufficientStockError(product_id, product["stock"])

    print("Покупку успішно оформлено!")
    print("Товар: " + product["name"])
    print("Кількість: " + str(quantity))


def buy_with_logging(product_id, quantity):
    try:
        buy_product(product_id, quantity)

    except ShopError:
        print("Помилку записано в журнал.")
        raise


def scene1():
    print("\n--- Завдання 1. Перевірка кількості товару ---")

    try:
        quantity = int(input("Введіть кількість товару: "))
        check_quantity(quantity)

        print("Кількість товару правильна.")

    except ValidationError as error:
        print(error)


def scene2():
    print("\n--- Завдання 2. Пошук товару ---")

    try:
        product_id = input("Введіть номер товару: ")
        product = find_product(product_id)

        print("Знайдено товар: " + product["name"])

    except ProductNotFoundError as error:
        print(error)
        print("Причина помилки:", error.__cause__)


def scene3():
    print("\n--- Завдання 3. Оформлення покупки ---")

    try:
        product_id = input("Введіть номер товару: ")
        quantity = int(input("Введіть кількість: "))

        buy_with_logging(product_id, quantity)

    except InsufficientStockError as error:
        print("Помилка покупки:", error)

    except ShopError as error:
        print("Інша помилка магазину:", error)


def scene4():
    print("\n--- Завдання 4. Перехоплення базового виключення ---")

    try:
        check_quantity(0)

    except ShopError as error:
        print("Перехоплено виключення магазину:")
        print(error)


scene1()
scene2()
scene3()
scene4()
