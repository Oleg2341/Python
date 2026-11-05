
numbers = [17, 83, 4, 56, 92, 31, 68, 11]

print("Початковий список:", numbers)

print("1. Індексація:")
print("Елемент з індексом 2:", numbers[2])
print("Елемент з індексом -1:", numbers[-1])

print("2. Зрізи:")
print("Перші чотири елементи:", numbers[:4])
print("Елементи з індексів 2 до 5:", numbers[2:6])
print("Кожен другий елемент:", numbers[::2])
print("Список у зворотному порядку:", numbers[::-1])

print("3. Додавання елемента:")
numbers.append(45)
print("Після додавання:", numbers)

print("4. Вставка елемента:")
numbers.insert(2, 73)
print("Після вставки:", numbers)

print("5. Видалення елемента:")
del numbers[4]
print("Після видалення:", numbers)

print("Фінальний список:", numbers)
print("Кількість елементів:", len(numbers))
