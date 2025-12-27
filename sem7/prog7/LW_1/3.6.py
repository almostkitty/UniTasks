import threading
import time
import random


class SafeQueue:
    def __init__(self):
        self.queue = []
        self.lock = threading.RLock()  # рекурсивный блокировщик

    def enqueue(self, item):
        with self.lock:
            self.queue.append(item)
            print(f"Добавлено: {item}, очередь: {self.queue}")

    def dequeue(self):
        with self.lock:
            if self.queue:
                item = self.queue.pop(0)
                print(f"Удалено: {item}, очередь: {self.queue}")
                return item
            else:
                print("Очередь пуста")
                return None

def producer(q: SafeQueue):
    for i in range(5):
        time.sleep(random.uniform(0.1, 0.5))
        q.enqueue(i)

def consumer(q: SafeQueue):
    for _ in range(5):
        time.sleep(random.uniform(0.2, 0.6))
        q.dequeue()

if __name__ == "__main__":
    q = SafeQueue()

    t1 = threading.Thread(target=producer, args=(q,))
    t2 = threading.Thread(target=consumer, args=(q,))
    t3 = threading.Thread(target=producer, args=(q,))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()
