
"""Створення та керування потоками в Python."""

import threading
import time


def download_simulation(file_name: str, size_mb: float) -> dict:
    """Імітація завантаження файлу (I/O-bound задача)."""

    thread_name = threading.current_thread().name

    print("[" + thread_name + "] Початок завантаження '" + file_name + "' (" + str(size_mb) + " MB)...")

    # Імітація завантаження залежно від розміру файлу
    time.sleep(size_mb * 0.5)

    print("[" + thread_name + "] Файл '" + file_name + "' завантажено.")

    return {
        "file": file_name,
        "size": size_mb,
        "thread": thread_name
    }


class MonitorThread(threading.Thread):
    """Потік-монітор, що періодично виводить стан системи."""

    def __init__(self, interval: float = 1.0):
        super().__init__(name="Monitor", daemon=True)
        self.interval = interval
        self._stop_event = threading.Event()

    def run(self):
        """Виводить кількість активних потоків."""

        while not self._stop_event.is_set():
            print("[Monitor] Активних потоків: " + str(threading.active_count()))
            self._stop_event.wait(self.interval)

    def stop(self):
        self._stop_event.set()


def main():
    files = [
        ("data.csv", 2.5),
        ("report.pdf", 1.0),
        ("image.png", 0.5),
        ("archive.zip", 4.0),
        ("log.txt", 0.3),
    ]

    # Створення та запуск демон-потоку
    monitor = MonitorThread(interval=1.0)
    monitor.start()

    # Створення потоків для завантаження файлів
    threads = []

    for file_name, size_mb in files:
        thread = threading.Thread(
            target=download_simulation,
            args=(file_name, size_mb)
        )
        threads.append(thread)

    # Паралельне виконання потоків
    start = time.perf_counter()

    for thread in threads:
        thread.start()

    # Очікування завершення всіх потоків
    for thread in threads:
        thread.join()

    elapsed = time.perf_counter() - start

    print("\nУсі файли завантажено за " + str(round(elapsed, 2)) + " сек")

    # Зупинка демон-потоку
    monitor.stop()

    # Послідовне виконання для порівняння
    print("\nПослідовне завантаження файлів:")

    start = time.perf_counter()

    for file_name, size_mb in files:
        download_simulation(file_name, size_mb)

    sequential_time = time.perf_counter() - start

    print("\nПослідовне виконання: " + str(round(sequential_time, 2)) + " сек")

    # Обчислення прискорення
    speedup = sequential_time / elapsed

    print("Прискорення: " + str(round(speedup, 2)) + " разів")


if __name__ == "__main__":
    main()
