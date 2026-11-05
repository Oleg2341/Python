
text = ""

print("Введіть текст. Для завершення введіть слово стоп:")

while True:
    line = input()
    if line.lower() == "стоп":
        break
    text += line + " "

print("Введений текст:")
print(text)

words = text.lower().split()

slovnyk = {}

for word in words:
    word = word.strip(".,!?;:()\"'")
    if word != "":
        slovnyk[word] = slovnyk.get(word, 0) + 1

print("Створений словник:")
print(slovnyk)

print("Кількість появ кожного слова:")

for word in sorted(slovnyk):
    print(word, "-", slovnyk[word])

print("Слова, які зустрічаються більше одного разу:")

popular = {}

for word, count in slovnyk.items():
    if count > 1:
        popular[word] = count

print("Окремий словник повторюваних слів:")
print(popular)

for word, count in sorted(popular.items()):
    print(word, "-", count)

print("Перевірка відсутнього слова:")
print("олег -", slovnyk.get("олег", 0))
