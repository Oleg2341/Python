
class FootballPlayer:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def play(self):
        return "Гравець бере участь у матчі"

    def __str__(self):
        return self.name + " (номер " + str(self.number) + ")"


class Goalkeeper(FootballPlayer):
    def __init__(self, name, number, saves):
        super().__init__(name, number)
        self.saves = saves

    def play(self):
        return "Воротар відбиває удари по воротах. Сейвів: " + str(self.saves)


class Defender(FootballPlayer):
    def __init__(self, name, number, tackles):
        super().__init__(name, number)
        self.tackles = tackles

    def play(self):
        return "Захисник зупиняє атаки суперника. Відборів: " + str(self.tackles)


class Forward(FootballPlayer):
    def __init__(self, name, number, goals):
        super().__init__(name, number)
        self.goals = goals

    def play(self):
        return "Нападник атакує ворота суперника. Забитих голів: " + str(self.goals)


players = [
    Goalkeeper("Thibaut Courtois", 1, 7),
    Defender("Sergio Ramos", 4, 5),
    Forward("Kylian Mbappe", 10, 2)
]

print("ФУТБОЛІСТИ КОМАНДИ")
print("--------------------")

for player in players:
    print(player)
    print(player.play())
    print()

print("ПЕРЕВІРКА ТИПІВ")
print("--------------------")

for player in players:
    print(player, "- футболіст:", isinstance(player, FootballPlayer))

print()

print("Goalkeeper є підкласом FootballPlayer:",
      issubclass(Goalkeeper, FootballPlayer))

print("Defender є підкласом FootballPlayer:",
      issubclass(Defender, FootballPlayer))

print("Forward є підкласом FootballPlayer:",
      issubclass(Forward, FootballPlayer))
