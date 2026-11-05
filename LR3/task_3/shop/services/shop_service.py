import shop.models.product as product_module

from ..models.exceptions import ValidationError
from ..models.exceptions import ProductNotFoundError
from ..models.exceptions import InsufficientStockError


class ShopService:
    def __init__(self):
        self.products = [
            product_module.Product("P001", "Ноутбук", 25000, 5),
            product_module.Product("P002", "Мишка", 500, 10),
            product_module.Product("P003", "Клавіатура", 1200, 7)
        ]

    def show_products(self):
        print("\nСписок товарів:")

        for product in self.products:
            print(product.product_id + " - " + str(product))

    def buy_product(self, product_id, quantity):
        if quantity <= 0:
            raise ValidationError("кількість товару")

        product = None

        for item in self.products:
            if item.product_id == product_id:
                product = item

        if product is None:
            raise ProductNotFoundError(product_id)

        if quantity > product.stock:
            raise InsufficientStockError(product.stock)

        total = product.price * quantity
        product.stock = product.stock - quantity

        print("\nПокупку успішно оформлено!")
        print("Товар: " + product.name)
        print("Кількість: " + str(quantity))
        print("До сплати: " + str(total) + " грн")