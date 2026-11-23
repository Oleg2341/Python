
import time

sizes = [500, 5000, 20000]
repeats = 5

print("Порівняння продуктивності структур даних\n")

print(f"{'N':<10}{'Пошук у списку':<22}{'Пошук у множині':<22}{'Пошук у dict':<22}")
print("-" * 76)

for n in sizes:
    data = list(range(n))
    my_set = set(data)
    my_dict = {x: x for x in data}

    target = n - 1
    attempts = 1000

    start = time.perf_counter()
    for _ in range(attempts):
        target in data
    list_time = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(attempts):
        target in my_set
    set_time = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(attempts):
        target in my_dict
    dict_time = time.perf_counter() - start

    list_time /= repeats
    set_time /= repeats
    dict_time /= repeats

    print(f"{n:<10}{list_time:<22.6f}{set_time:<22.6f}{dict_time:<22.6f}")

print("\nПорівняння побудови унікальних значень\n")

print(f"{'N':<10}{'Список':<22}{'Множина':<22}")
print("-" * 54)

for n in sizes:
    data = [i % (n // 2) for i in range(n)]

    list_total = 0
    set_total = 0

    for _ in range(repeats):
        start = time.perf_counter()

        unique_list = []
        for item in data:
            if item not in unique_list:
                unique_list.append(item)

        list_total += time.perf_counter() - start

        start = time.perf_counter()

        unique_set = set()
        for item in data:
            unique_set.add(item)

        set_total += time.perf_counter() - start

    list_time = list_total / repeats
    set_time = set_total / repeats

    print(f"{n:<10}{list_time:<22.6f}{set_time:<22.6f}")

print("\nПеревірка результатів:")
print("Кількість унікальних елементів у списку:", len(unique_list))
print("Кількість унікальних елементів у множині:", len(unique_set))
