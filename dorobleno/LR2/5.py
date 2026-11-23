
class Observer:
    def update(self, event):
        pass


class Commentator(Observer):
    def update(self, event):
        print("Коментатор:", event)


class Journalist(Observer):
    def update(self, event):
        print("Журналіст отримав новину:", event)


class Fan(Observer):
    def update(self, event):
        print("Вболівальник:", event)


class FootballMatch:
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
        self.observers = []
        self.score = [0, 0]

    def subscribe(self, observer):
        self.observers.append(observer)

    def unsubscribe(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify(self, event):
        for observer in self.observers:
            observer.update(event)

    def goal(self, team):
        if team == self.home_team:
            self.score[0] += 1
        elif team == self.away_team:
            self.score[1] += 1
        else:
            print("Такої команди немає!")
            return

        event = f"ГОЛ! {team} забиває! Рахунок: {self.score[0]}:{self.score[1]}"
        self.notify(event)


match = FootballMatch("Динамо", "Шахтар")

commentator = Commentator()
journalist = Journalist()
fan = Fan()

match.subscribe(commentator)
match.subscribe(journalist)
match.subscribe(fan)

print("Початок футбольного матчу")
print("Динамо - Шахтар")

match.goal("Динамо")

print("\nВідписка журналіста")
match.unsubscribe(journalist)

match.goal("Шахтар")

print("\nДодавання нового спостерігача")

class Coach(Observer):
    def update(self, event):
        print("Тренер аналізує подію:", event)


coach = Coach()
match.subscribe(coach)

match.goal("Динамо")
