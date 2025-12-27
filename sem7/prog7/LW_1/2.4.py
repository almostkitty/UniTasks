import threading
from math import prod


def factorial_range(start, end, result, index):
    result[index] = prod(range(start, end + 1))

n = 10
n_threads = 2
chunk = n // n_threads
results = [1] * n_threads
threads = []

for i in range(n_threads):
    start = i * chunk + 1
    end = (i + 1) * chunk if i < n_threads - 1 else n
    t = threading.Thread(target=factorial_range, args=(start, end, results, i))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

factorial = prod(results)
print(f"Факториал {n} = {factorial}")
