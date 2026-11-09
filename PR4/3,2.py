
"""Producer-Consumer з queue.Queue та демонстрація дедлоку."""

import threading
import queue
import time
import random


class Task:
    """Завдання для обробки."""

    def __init__(self, task_id: int, data: str, priority: int = 0):
        self.task_id = task_id
        self.data = data
        self.priority = priority
        self.created_at = time.time()

    def __repr__(self):
        return "Task(id=" + str(self.task_id) + ", data='" + self.data + "')"


def producer(task_queue: queue.Queue, num_tasks: int,
             producer_id: int) -> None:
    """Виробник генерує завдання та поміщає їх у чергу."""

    for i in range(num_tasks):
        task = Task(
            task_id=producer_id * 100 + i,
            data="Дані від виробника " + str(producer_id) + ", пакет " + str(i),
            priority=random.randint(1, 5),
        )

        task_queue.put(task)

        print("[Виробник-" + str(producer_id) +
              "] Створено завдання:", task)

        time.sleep(random.uniform(0.1, 0.3))

    print("[Виробник-" + str(producer_id) + "] Завершив роботу")


def consumer(task_queue: queue.Queue, consumer_id: int,
             results: list, results_lock: threading.Lock) -> None:
    """Споживач обробляє завдання з черги."""

    while True:
        try:
            task = task_queue.get(timeout=2)

        except queue.Empty:
            print("[Споживач-" + str(consumer_id) +
                  "] Черга порожня, завершення")
            break

        if task is None:
            task_queue.task_done()
            task_queue.put(None)
            break

        # Імітація обробки завдання
        print("[Споживач-" + str(consumer_id) +
              "] Обробляє завдання:", task)

        time.sleep(random.uniform(0.2, 0.5))

        result = {
            "task_id": task.task_id,
            "consumer": consumer_id,
            "time": time.time() - task.created_at
        }

        # Збереження результату
        with results_lock:
            results.append(result)

        print("[Споживач-" + str(consumer_id) +
              "] Завдання виконано:", task.task_id)

        task_queue.task_done()


def producer_consumer_demo():
    """Демонстрація паттерну Producer-Consumer."""

    task_queue = queue.Queue(maxsize=5)
    results = []
    results_lock = threading.Lock()

    num_producers = 2
    num_consumers = 3
    tasks_per_producer = 5

    producers = []
    consumers = []

    # Створення споживачів
    for i in range(num_consumers):
        t = threading.Thread(
            target=consumer,
            args=(task_queue, i + 1, results, results_lock)
        )
        consumers.append(t)
        t.start()

    # Створення виробників
    for i in range(num_producers):
        t = threading.Thread(
            target=producer,
            args=(task_queue, tasks_per_producer, i + 1)
        )
        producers.append(t)
        t.start()

    # Очікування завершення виробників
    for t in producers:
        t.join()

    # Додавання сигналів завершення
    for i in range(num_consumers):
        task_queue.put(None)

    # Очікування завершення споживачів
    for t in consumers:
        t.join()

    # Виведення результатів
    print("\n=== Результати обробки ===")
    print("Кількість оброблених задач:", len(results))

    if len(results) > 0:
        total_time = sum(result["time"] for result in results)
        average_time = total_time / len(results)

        print("Середній час обробки:",
              round(average_time, 3), "сек")


def deadlock_demo():
    """Демонстрація та виявлення потенційного дедлоку."""

    lock_a = threading.Lock()
    lock_b = threading.Lock()
    deadlock_detected = threading.Event()

    def worker_1():
        lock_a.acquire()
        print("[Worker-1] Захопив Lock A")

        time.sleep(0.1)

        acquired = lock_b.acquire(timeout=2)

        if not acquired:
            print("[Worker-1] ДЕДЛОК: не вдалося захопити Lock B!")
            deadlock_detected.set()
            lock_a.release()
            return

        print("[Worker-1] Захопив Lock B")

        lock_b.release()
        lock_a.release()

    def worker_2():
        lock_b.acquire()
        print("[Worker-2] Захопив Lock B")

        time.sleep(0.1)

        acquired = lock_a.acquire(timeout=2)

        if not acquired:
            print("[Worker-2] ДЕДЛОК: не вдалося захопити Lock A!")
            deadlock_detected.set()
            lock_b.release()
            return

        print("[Worker-2] Захопив Lock A")

        lock_a.release()
        lock_b.release()

    def safe_worker_1():
        """Безпечне захоплення замків у порядку A -> B."""

        with lock_a:
            print("[Safe Worker-1] Захопив Lock A")

            with lock_b:
                print("[Safe Worker-1] Захопив Lock B")
                time.sleep(0.1)

    def safe_worker_2():
        """Безпечне захоплення замків у порядку A -> B."""

        with lock_a:
            print("[Safe Worker-2] Захопив Lock A")

            with lock_b:
                print("[Safe Worker-2] Захопив Lock B")
                time.sleep(0.1)

    # Демонстрація потенційного дедлоку
    print("=== Спроба з потенційним дедлоком ===")

    t1 = threading.Thread(target=worker_1)
    t2 = threading.Thread(target=worker_2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    if deadlock_detected.is_set():
        print(">>> Дедлок виявлено! Використовуємо timeout.\n")
    else:
        print(">>> Дедлок не виник цього разу.\n")

    # Безпечна версія
    print("=== Безпечна версія (однаковий порядок замків) ===")

    t1 = threading.Thread(target=safe_worker_1)
    t2 = threading.Thread(target=safe_worker_2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(">>> Безпечне виконання завершено без дедлоку.")


def main():
    print("=" * 60)
    print("=== Паттерн Producer-Consumer ===")
    print("=" * 60)

    producer_consumer_demo()

    print("\n" + "=" * 60)
    print("=== Демонстрація дедлоку ===")
    print("=" * 60)

    deadlock_demo()


if __name__ == "__main__":
    main()
