
"""Демонстрація race condition та захист через Lock."""

import threading
import time
import random


class BankAccount:
    """Банківський рахунок без синхронізації."""

    def __init__(self, balance: float = 0.0):
        self.balance = balance
        self.transaction_count = 0

    def deposit(self, amount: float) -> None:
        """Поповнення рахунку."""

        current = self.balance
        time.sleep(random.uniform(0.0001, 0.001))
        self.balance = current + amount
        self.transaction_count += 1

    def withdraw(self, amount: float) -> bool:
        """Зняття коштів."""

        current = self.balance
        time.sleep(random.uniform(0.0001, 0.001))

        if current >= amount:
            self.balance = current - amount
            self.transaction_count += 1
            return True

        return False


class SafeBankAccount:
    """Банківський рахунок із синхронізацією через Lock."""

    def __init__(self, balance: float = 0.0):
        self.balance = balance
        self.transaction_count = 0
        self._lock = threading.Lock()

    def deposit(self, amount: float) -> None:
        """Поповнення рахунку з блокуванням."""

        with self._lock:
            current = self.balance
            time.sleep(random.uniform(0.0001, 0.001))
            self.balance = current + amount
            self.transaction_count += 1

    def withdraw(self, amount: float) -> bool:
        """Зняття коштів із блокуванням."""

        with self._lock:
            current = self.balance
            time.sleep(random.uniform(0.0001, 0.001))

            if current >= amount:
                self.balance = current - amount
                self.transaction_count += 1
                return True

            return False


def run_transactions(account, num_deposits: int, num_withdrawals: int):
    """Запускає потоки для виконання транзакцій."""

    threads = []

    # Створення потоків для поповнення
    for i in range(5):
        thread = threading.Thread(
            target=lambda: [account.deposit(50.0) for _ in range(num_deposits // 5)]
        )
        threads.append(thread)

    # Створення потоків для зняття коштів
    for i in range(5):
        thread = threading.Thread(
            target=lambda: [account.withdraw(50.0) for _ in range(num_withdrawals // 5)]
        )
        threads.append(thread)

    # Запуск потоків
    for thread in threads:
        thread.start()

    # Очікування завершення
    for thread in threads:
        thread.join()


def main():
    initial_balance = 1000.0
    num_deposits = 100
    deposit_amount = 50.0
    num_withdrawals = 100
    withdraw_amount = 50.0

    expected_balance = (
        initial_balance
        + num_deposits * deposit_amount
        - num_withdrawals * withdraw_amount
    )

    # Тест без синхронізації
    print("=== Тест без синхронізації ===")

    unsafe_account = BankAccount(initial_balance)

    run_transactions(unsafe_account, num_deposits, num_withdrawals)

    print("Очікуваний баланс:", expected_balance)
    print("Фактичний баланс:", unsafe_account.balance)
    print("Кількість транзакцій:", unsafe_account.transaction_count)
    print("Результат правильний:", unsafe_account.balance == expected_balance)

    # Тест із синхронізацією
    print("\n=== Тест із синхронізацією (Lock) ===")

    safe_account = SafeBankAccount(initial_balance)

    run_transactions(safe_account, num_deposits, num_withdrawals)

    print("Очікуваний баланс:", expected_balance)
    print("Фактичний баланс:", safe_account.balance)
    print("Кількість транзакцій:", safe_account.transaction_count)
    print("Результат правильний:", safe_account.balance == expected_balance)

    print("\nОчікуваний баланс: " + str(round(expected_balance, 2)))


if __name__ == "__main__":
    main()
