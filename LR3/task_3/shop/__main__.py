from shop import *

def main():
    print("ІНТЕРНЕТ-МАГАЗИН")

    shop = ShopService()

    shop.show_products()

    try:
        product_id = input("\nВведіть номер товару: ")
        quantity = int(input("Введіть кількість: "))

        shop.buy_product(product_id, quantity)

    except ValueError:
        print("Помилка! Потрібно ввести ціле число.")


    print("\nПеревірка __all__:")
    print("Product:", "Product" in globals())
    print("ShopService:", "ShopService" in globals())
    print("models:", "models" in globals())


if __name__ == "__main__":
    main()