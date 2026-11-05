
from abc import ABC, abstractmethod


class FootballPlayer(ABC):
    def __init__(self, name, number):
        self.name = name
        self.number = number

    @property
    @abstractmethod
    def position(self):
        pass

    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def train(self):
        pass

    def info(self):
        print("Ім'я:", self.name)
        print("Номер:", self.number)
        print("Позиція:", self.position)


class Forward(FootballPlayer):
    @property
    def position(self):
        return "Нападник"

    def play(self):
        print(self.name, "забиває голи")

    def train(self):
        print(self.name, "тренує удари")


class Goalkeeper(FootballPlayer):
    @property
    def position(self):
        return "Воротар"

    def play(self):
        print(self.name, "захищає ворота")

    def train(self):
        print(self.name, "тренує реакцію")


class Coach:
    def __init__(self, name):
        self.name = name

    def train_team(self):
        print(self.name, "проводить тренування")


class Team:
    def __init__(self, name, coach):
        self.name = name
        self.coach = coach
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def show_team(self):
        print("\nКоманда:", self.name)

        for player in self.players:
            player.info()
            player.play()
            print()

    def training(self):
        self.coach.train_team()

        for player in self.players:
            player.train()


try:
    test = FootballPlayer("Test", 10)
except TypeError:
    print("Не можна створити об'єкт абстрактного класу")


player1 = Forward("Kylian Mbappe", 10)
player2 = Goalkeeper("Thibaut Courtois", 1)

print("\nПоліморфізм:")

player1.play()
player2.play()

coach = Coach("Carlo Ancelotti")

team = Team("Real Madrid", coach)

team.add_player(player1)
team.add_player(player2)

team.show_team()

print("Тренування:")
team.training()
