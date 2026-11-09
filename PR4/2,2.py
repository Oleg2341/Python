
"""Семафори та Event для управління конкурентним доступом."""

import threading
import time
import random


class ConnectionPool:
    """Пул з'єднань з обмеженням через Semaphore."""

    def __init__(self, max_connections: int = 3):
        self._semaphore = threading.Semaphore(max_connections)
        self._lock = threading.Lock()
        self.max_connections = max_connections
        self.active_connections = 0
        self.total_served = 0
        self.peak_connections = 0

    def acquire_connection(self, client_name: str) -> None:
        """Отримання з'єднання."""

        print("[" + client_name + "] Запит на з'єднання...")

        # Очікування вільного з'єднання
        self._semaphore.acquire()

        with self._lock:
            self.active_connections += 1

            if self.active_connections > self.peak_connections:
                self.peak_connections = self.active_connections

    def release_connection(self, client_name: str) -> None:
        """Повернення з'єднання до пулу."""

        with self._lock:
            self.active_connections -= 1
            self.total_served += 1

        print("[" + client_name + "] З'єднання звільнено.")

        self._semaphore.release()

    def get_stats(self) -> dict:
        """Повертає статистику використання пулу."""

        with self._lock:
            return {
                "max": self.max_connections,
                "active": self.active_connections,
                "total_served": self.total_served,
                "peak": self.peak_connections,
            }


def client_task(pool: ConnectionPool, client_name: str,
                ready_event: threading.Event) -> None:
    """Клієнт, що очікує сигналу готовності."""

    # Очікування сигналу від сервера
    ready_event.wait()

    pool.acquire_connection(client_name)

    try:
        work_time = random.uniform(0.5, 2.0)

        print("  [" + client_name + "] Працює " +
              str(round(work_time, 1)) + " сек " +
              "(активних: " + str(pool.active_connections) + ")")

        time.sleep(work_time)

    finally:
        pool.release_connection(client_name)


def main():
    pool = ConnectionPool(max_connections=3)
    ready_event = threading.Event()
    num_clients = 10

    # Створення та запуск клієнтських потоків
    threads = []

    for i in range(num_clients):
        t = threading.Thread(
            target=client_task,
            args=(pool, "Client-" + str(i).zfill(2), ready_event)
        )

        threads.append(t)
        t.start()

    # Очікування запуску всіх потоків
    time.sleep(0.5)

    print("\n>>> Сервер готовий! Усі клієнти починають роботу.\n")

    # Сигнал для початку роботи клієнтів
    ready_event.set()

    # Очікування завершення всіх потоків
    for t in threads:
        t.join()

    # Отримання статистики
    stats = pool.get_stats()

    print("\n=== Статистика пулу ===")
    print("Макс. з'єднань:", stats["max"])
    print("Активних з'єднань:", stats["active"])
    print("Обслуговано клієнтів:", stats["total_served"])
    print("Пікове навантаження:", stats["peak"])

    print("\nПеревищення ліміту:",
          stats["peak"] > stats["max"])

    print("Усі клієнти обслуговані:",
          stats["total_served"] == num_clients)


if __name__ == "__main__":
    main()
