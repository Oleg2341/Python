
class FootballPlayer:
    def __init__(self, name, goals, assists):
        self.name = name
        self.goals = goals
        self.assists = assists

    def __str__(self):
        return f"{self.name}: голи - {self.goals}, асисти - {self.assists}"

    def __repr__(self):
        return f"FootballPlayer('{self.name}', {self.goals}, {self.assists})"

    def __add__(self, other):
        return FootballPlayer(self.name, self.goals + other.goals, self.assists + other.assists)

    def __sub__(self, other):
        return FootballPlayer(self.name, self.goals - other.goals, self.assists - other.assists)

    def __mul__(self, number):
        return FootballPlayer(self.name, self.goals * number, self.assists * number)

    def __eq__(self, other):
        return self.goals + self.assists == other.goals + other.assists

    def __lt__(self, other):
        return self.goals + self.assists < other.goals + other.assists

    def __len__(self):
        return self.goals + self.assists


player1 = FootballPlayer("Messi", 20, 15)
player2 = FootballPlayer("Ronaldo", 25, 10)

print("Перший гравець:")
print(player1)

print("\nПредставлення об'єкта:")
print(repr(player1))

print("\nДодавання статистики:")
print(player1 + player2)

print("\nВіднімання статистики:")
print(player1 - player2)

print("\nМноження статистики:")
print(player1 * 2)

print("\nПорівняння гравців:")
print(player1 == player2)
print(player1 < player2)

print("\nКількість результативних дій:")
print(len(player1))
