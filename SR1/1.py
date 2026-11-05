# Функція для підрахунку загальної кількості голів
def calculate_goals(goals):
    total = 0

    # Цикл for для перебору списку голів
    for goal in goals:
        total += goal

    return total


# Функція для розрахунку очок футболіста
def player_points(goals, assists):
    return goals * 2 + assists


# Функція для пошуку найкращого футболіста
def best_player(players):
    best = players[0]

    # Перебір словників зі списку
    for player in players:
        if player["points"] > best["points"]:
            best = player

    return best


# Генератор для перебору футболістів
def player_generator(players):
    for player in players:
        yield player


def main():

    # Список словників з інформацією про футболістів
    players = [
        {"name": "Lionel Messi", "goals": 20, "assists": 15},
        {"name": "Cristiano Ronaldo", "goals": 25, "assists": 5},
        {"name": "Kylian Mbappe", "goals": 18, "assists": 8},
        {"name": "Erling Haaland", "goals": 22, "assists": 4},
        {"name": "Lamine Yamal", "goals": 10, "assists": 12}
    ]

    # Обчислення очок для кожного футболіста
    for player in players:
        player["points"] = player_points(player["goals"], player["assists"])

    # Кортеж з назвами футбольних команд
    team = ("Real Madrid", "Barcelona", "Manchester City")

    # Цикл while для роботи меню програми
    while True:
        print("\n=== ФУТБОЛЬНИЙ МЕНЕДЖЕР ===")
        print("1. Переглянути футболістів")
        print("2. Додати футболіста")
        print("3. Загальна статистика")
        print("4. Найкращий футболіст")
        print("5. Переглянути команди")
        print("6. Ітератор та генератор")
        print("0. Вихід")

        choice = input("Ваш вибір: ")

        # Умовні оператори if та elif
        if choice == "1":
            print("\nСписок футболістів:")

            # Цикл for для виведення списку
            for player in players:
                print(player["name"] + ": голи - " + str(player["goals"]) +
                      ", асисти - " + str(player["assists"]))

        elif choice == "2":
            # Введення даних користувачем
            name = input("Ім'я футболіста: ")
            goals = int(input("Кількість голів: "))
            assists = int(input("Кількість асистів: "))

            # Перевірка введених значень
            if goals < 0 or assists < 0:
                print("Статистика не може бути від'ємною")
            else:
                # Створення нового словника
                player = {
                    "name": name,
                    "goals": goals,
                    "assists": assists,
                    "points": player_points(goals, assists)
                }

                # Додавання футболіста до списку
                players.append(player)
                print("Футболіста додано")

        elif choice == "3":
            # Створення списку для зберігання голів
            goals = []

            for player in players:
                goals.append(player["goals"])

            # Використання функції len() та власної функції
            print("Кількість футболістів: " + str(len(players)))
            print("Всього голів: " + str(calculate_goals(goals)))

            # Підрахунок загальної кількості асистів
            assists = 0

            for player in players:
                assists += player["assists"]

            print("Всього асистів: " + str(assists))

        elif choice == "4":
            # Перевірка, чи є футболісти у списку
            if len(players) > 0:
                player = best_player(players)

                print("Найкращий футболіст: " + player["name"])
                print("Голи: " + str(player["goals"]))
                print("Асисти: " + str(player["assists"]))
                print("Очки: " + str(player["points"]))
            else:
                print("Список футболістів порожній")

        elif choice == "5":
            print("\nСписок команд:")

            # Перебір елементів кортежу
            for club in team:
                print(club)

        elif choice == "6":
            print("\nРобота з ітератором:")

            # Створення ітератора зі списку футболістів
            iterator = iter(players)

            # Функція next() отримує наступний елемент ітератора
            for i in range(len(players)):
                player = next(iterator)
                print(player["name"])

            print("\nРобота з генератором:")

            # Використання генератора
            for player in player_generator(players):
                print(player["name"])

        elif choice == "0":
            print("Програму завершено")

            # break завершує цикл while
            break

        else:
            print("Неправильний вибір")


# Перевірка запуску основної функції
if __name__ == "__main__":
    main()