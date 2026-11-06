"""Паттерни Observer, Strategy та архітектурний шаблон MVC."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable


# --- Observer ---

class EventEmitter:
    """Базовий клас для підтримки системи подій."""

    def __init__(self):
        self._listeners = {}

    def on(self, event, callback):
        if event not in self._listeners:
            self._listeners[event] = []

        self._listeners[event].append(callback)

    def off(self, event, callback):
        if event in self._listeners:
            if callback in self._listeners[event]:
                self._listeners[event].remove(callback)

    def emit(self, event, *args, **kwargs):
        if event in self._listeners:
            for callback in self._listeners[event]:
                callback(*args, **kwargs)


# --- Strategy ---

class SortStrategy(ABC):
    """Абстрактна стратегія сортування завдань."""

    @abstractmethod
    def sort(self, tasks):
        pass


class SortByPriority(SortStrategy):
    """Сортування за пріоритетом."""

    def sort(self, tasks):
        return sorted(tasks, key=lambda task: task.priority)


class SortByDeadline(SortStrategy):
    """Сортування за терміном виконання."""

    def sort(self, tasks):
        return sorted(tasks, key=lambda task: task.deadline)


class SortByCreationDate(SortStrategy):
    """Сортування за датою створення."""

    def sort(self, tasks):
        return sorted(tasks, key=lambda task: task.created_at, reverse=True)


# --- Model ---

@dataclass
class Task:
    title: str
    priority: int
    deadline: datetime
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)


class TaskModel(EventEmitter):
    """Модель для роботи із завданнями."""

    def __init__(self):
        super().__init__()
        self._tasks = []

    def add_task(self, title, priority, deadline):
        if priority < 1 or priority > 5:
            raise ValueError("Пріоритет повинен бути від 1 до 5")

        task = Task(title, priority, deadline)
        self._tasks.append(task)

        self.emit("task_added", task)

    def complete_task(self, index):
        if index < 0 or index >= len(self._tasks):
            raise IndexError("Завдання не знайдено")

        task = self._tasks[index]
        task.completed = True

        self.emit("task_completed", task)

    def remove_task(self, index):
        if index < 0 or index >= len(self._tasks):
            raise IndexError("Завдання не знайдено")

        task = self._tasks.pop(index)

        self.emit("task_removed", task)

    def get_tasks(self, include_completed=True):
        if include_completed:
            return self._tasks[:]

        return [task for task in self._tasks if not task.completed]

    def get_statistics(self):
        total = len(self._tasks)
        completed = len([task for task in self._tasks if task.completed])
        active = total - completed

        return {
            "total": total,
            "completed": completed,
            "active": active
        }


# --- View ---

class TaskView:
    """Відображення даних у консолі."""

    def show_tasks(self, tasks, title="Завдання"):
        print("\n" + title)
        print("-" * 85)
        print("№ | Назва | Пріоритет | Дедлайн | Статус")
        print("-" * 85)

        for i, task in enumerate(tasks, 1):
            if task.completed:
                status = "Виконано"
            else:
                status = "Активне"

            print(str(i) + " | " + task.title +
                  " | " + str(task.priority) +
                  " | " + task.deadline.strftime("%d.%m.%Y") +
                  " | " + status)

        print("-" * 85)

    def show_message(self, message):
        print("[INFO] " + message)

    def show_statistics(self, stats):
        print("\nСтатистика завдань:")
        print("Всього: " + str(stats["total"]))
        print("Виконано: " + str(stats["completed"]))
        print("Активних: " + str(stats["active"]))


# --- Controller ---

class TaskController:
    """Контролер для координації моделі та вигляду."""

    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._sort_strategy = SortByPriority()

        self._model.on(
            "task_added",
            lambda task: self._view.show_message(
                "Додано завдання: " + task.title
            )
        )

        self._model.on(
            "task_completed",
            lambda task: self._view.show_message(
                "Завдання виконано: " + task.title
            )
        )

        self._model.on(
            "task_removed",
            lambda task: self._view.show_message(
                "Видалено завдання: " + task.title
            )
        )

    def set_sort_strategy(self, strategy):
        self._sort_strategy = strategy

    def add_task(self, title, priority, deadline):
        self._model.add_task(title, priority, deadline)

    def complete_task(self, index):
        self._model.complete_task(index)

    def show_all(self):
        tasks = self._model.get_tasks()
        sorted_tasks = self._sort_strategy.sort(tasks)
        self._view.show_tasks(sorted_tasks)

    def show_active(self):
        tasks = self._model.get_tasks(include_completed=False)
        sorted_tasks = self._sort_strategy.sort(tasks)
        self._view.show_tasks(sorted_tasks, title="Активні завдання")

    def show_stats(self):
        self._view.show_statistics(self._model.get_statistics())


def main():
    model = TaskModel()
    view = TaskView()
    ctrl = TaskController(model, view)

    print("Додавання завдань:")

    ctrl.add_task("Виконати лабораторну роботу", 1, datetime(2026, 11, 10))
    ctrl.add_task("Підготувати презентацію", 2, datetime(2026, 11, 12))
    ctrl.add_task("Вивчити Python", 3, datetime(2026, 11, 15))
    ctrl.add_task("Зробити домашнє завдання", 1, datetime(2026, 11, 8))
    ctrl.add_task("Прочитати книгу", 5, datetime(2026, 11, 20))

    print("\nСортування за пріоритетом:")
    ctrl.show_all()

    print("\nСортування за дедлайном:")
    ctrl.set_sort_strategy(SortByDeadline())
    ctrl.show_all()

    print("\nПозначення завдання як виконаного:")
    ctrl.complete_task(0)

    print("\nАктивні завдання:")
    ctrl.show_active()

    print("\nСортування за датою створення:")
    ctrl.set_sort_strategy(SortByCreationDate())
    ctrl.show_all()

    print("\nЗагальна статистика:")
    ctrl.show_stats()


if __name__ == "__main__":
    main()