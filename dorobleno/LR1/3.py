
text = ""

print("Введіть текст. Для завершення введіть слово стоп:")

while True:
    line = input()
    if line.lower() == "стоп":
        break
    text += line + " "

print("\nВведений текст:")
print(text)

words = text.lower().split()

slovnyk = {}

for word in words:
    word = word.strip(".,!?;:()\"'")
    if word != "":
        slovnyk[word] = slovnyk.get(word, 0) + 1

print("\nСтворений словник:")
print(slovnyk)

print("\nКількість появ кожного слова:")

for word in sorted(slovnyk):
    print(word, "-", slovnyk[word])

popular = {word: count for word, count in slovnyk.items() if count > 1}

print("\nСлова, які зустрічаються більше одного разу:")
print(popular)

for word, count in sorted(popular.items()):
    print(word, "-", count)

print("\nСортування за спаданням частоти:")

for word, count in sorted(slovnyk.items(), key=lambda item: (-item[1], item[0])):
    print(word, "-", count)

print("\nПеревірка відсутнього слова:")
print("олег -", slovnyk.get("олег", 0))
