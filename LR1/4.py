list1 = [1, 2, 3, 4, 2, 5, 6]
list2 = [3, 4, 5, 7, 7, 8]
list3 = [1, 2, 3]

set1 = set(list1)
set2 = set(list2)
set3 = set(list3)

print("Початкові множини:")
print("Множина 1:", list1)
print("Множина 2:", list2)
print("Множина 3:", list3)

print("\nМножини унікальних значень:")
print("Множина 1:", sorted(set1))
print("Множина 2:", sorted(set2))
print("Множина 3:", sorted(set3))

print("\nОперації над множинами:")

print("Перетин множин 1 і 2:", sorted(set1 & set2))

print("Об'єднання множин 1 і 2:", sorted(set1 | set2))

print("Симетрична різниця множин 1 і 2:", sorted(set1 ^ set2))

print("\nПеревірка підмножин:")

print("Множина 3 є підмножиною множини 1:", set3 <= set1)

print("Множина 2 є підмножиною множини 1:", set2 <= set1)
