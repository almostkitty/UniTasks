import threading
import time
import random


class BankAccount:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
        self.lock = threading.Lock()  # Lock для синхронизации

    def deposit(self, amount):
        with self.lock:  # Захватываем блокировку
            old_balance = self.balance
            time.sleep(0.01)  # имитация задержки
            self.balance = old_balance + amount
            print(f"Пополнение: {amount}, баланс: {self.balance}")

    def withdraw(self, amount):
        with self.lock:  # Захватываем блокировку
            if self.balance >= amount:
                old_balance = self.balance
                time.sleep(0.01)  # имитация задержки
                self.balance = old_balance - amount
                print(f"Снятие: {amount}, баланс: {self.balance}")
            else:
                print(f"Недостаточно средств для снятия {amount}, баланс: {self.balance}")

# ---------------------------
# Основная симуляция
# ---------------------------
if __name__ == "__main__":
    account = BankAccount(1000)  # начальный баланс
    threads = []

    # 10 потоков которые пополняют счёт
    for _ in range(10):
        t = threading.Thread(target=lambda: account.deposit(random.randint(10, 50)))
        threads.append(t)

    # 10 потоков, которые снимают деньги
    for _ in range(10):
        t = threading.Thread(target=lambda: account.withdraw(random.randint(1, 100)))
        threads.append(t)

    # запускаем все потоки
    for t in threads:
        t.start()

    # ждём завершения всех потоков
    for t in threads:
        t.join()

    print(f"Итоговый баланс: {account.balance}")
