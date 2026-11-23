
"""Модуль для управління футбольною командою та її гравцями."""

from typing import Optional


class Player:
    """Клас для представлення футбольного гравця.

    Attributes:
        name (str): Ім'я гравця.
        position (str): Позиція гравця.
        number (int): Ігровий номер.
        goals (int): Кількість забитих голів.
    """

    def __init__(self, name: str, position: str, number: int) -> None:
        """Створює нового футбольного гравця.

        Args:
            name (str): Ім'я гравця.
            position (str): Позиція гравця.
            number (int): Ігровий номер.

        Raises:
            ValueError: Якщо ім'я порожнє або номер некоректний.
        """
        if not name.strip() or not position.strip() or not 1 <= number <= 99:
            raise ValueError("Некоректні дані гравця")

        self.name = name
        self.position = position
        self.number = number
        self.goals = 0

    def score_goal(self) -> int:
        """Збільшує кількість забитих гравцем голів.

        Returns:
            int: Нова кількість голів.

        Raises:
            Немає.
        """
        self.goals += 1
        return self.goals

    def get_info(self) -> str:
        """Повертає інформацію про гравця.

        Returns:
            str: Інформація про гравця.
        """
        return (
            f"{self.name}, позиція: {self.position}, "
            f"номер: {self.number}, голи: {self.goals}"
        )


class Team:
    """Клас для представлення футбольної команди.

    Attributes:
        name (str): Назва команди.
        players (list[Player]): Список гравців команди.
    """

    def __init__(self, name: str) -> None:
        """Створює футбольну команду.

        Args:
            name (str): Назва команди.

        Raises:
            ValueError: Якщо назва команди порожня.
        """
        if not name.strip():
            raise ValueError("Назва команди не може бути порожньою")

        self.name = name
        self.players: list[Player] = []

    def add_player(self, player: Player) -> None:
        """Додає гравця до команди.

        Args:
            player (Player): Гравець для додавання.

        Raises:
            ValueError: Якщо гравець із таким номером уже існує.
        """
        if any(p.number == player.number for p in self.players):
            raise ValueError("Гравець із таким номером уже існує")

        self.players.append(player)

    def find_player(self, name: str) -> Optional[Player]:
        """Знаходить гравця за ім'ям.

        Args:
            name (str): Ім'я гравця.

        Returns:
            Optional[Player]: Знайдений гравець або None.
        """
        for player in self.players:
            if player.name.lower() == name.lower():
                return player
        return None

    def get_players(self) -> list[str]:
        """Повертає список імен гравців команди.

        Returns:
            list[str]: Список імен гравців.
        """
        return [player.name for player in self.players]

    def get_team_info(self) -> str:
        """Формує інформацію про команду та її гравців.

        Returns:
            str: Повна інформація про команду.
        """
        result = f"Команда: {self.name}\n"

        for player in self.players:
            result += player.get_info() + "\n"

        return result


def main() -> None:
    """Демонструє роботу системи футбольної команди.

    Returns:
        None: Функція нічого не повертає.

    Raises:
        ValueError: Якщо передано некоректні дані.
    """
    team = Team("Динамо Київ")

    player1 = Player("Андрій", "Нападник", 9)
    player2 = Player("Олександр", "Півзахисник", 10)
    player3 = Player("Максим", "Захисник", 4)

    team.add_player(player1)
    team.add_player(player2)
    team.add_player(player3)

    player1.score_goal()
    player1.score_goal()
    player2.score_goal()

    print(team.get_team_info())
    print("Список гравців:", team.get_players())

    found = team.find_player("Андрій")

    if found:
        print("Знайдений гравець:", found.get_info())

    print("\n--- Інтроспекція ---")
    print("Назва класу:", Player.__name__)
    print("Документація класу:", Player.__doc__)
    print("Анотації:", Player.__init__.__annotations__)

    print("\n--- HELP ---")
    help(Player)


if __name__ == "__main__":
    main()
