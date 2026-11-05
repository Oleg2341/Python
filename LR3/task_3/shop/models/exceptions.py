class ShopError(Exception):
    pass


class ValidationError(ShopError):
    def __init__(self, field):
        self.field = field

    def __str__(self):
        return "Помилка введення: " + self.field


class ProductNotFoundError(ShopError):
    def __init__(self, product_id):
        self.product_id = product_id

    def __str__(self):
        return "Товар " + self.product_id + " не знайдено."


class InsufficientStockError(ShopError):
    def __init__(self, available):
        self.available = available

    def __str__(self):
        return "Недостатньо товару. Доступно: " + str(self.available)