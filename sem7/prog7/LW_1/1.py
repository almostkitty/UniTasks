import math
import timeit
import threading


# Последовательные функции
def integrate(f, a, b, *, n_iter=1000):
    """Численное интегрирование методом прямоугольников"""
    h = (b - a) / n_iter
    total = 0
    for i in range(n_iter):
        total += f(a + i*h) * h
    return total

def integrate2(f, a, b, n_iter=1000):
    """Альтернативная реализация через sum"""
    h = (b - a) / n_iter
    return sum(f(a + i*h) * h for i in range(n_iter))

# Многопоточная версия
def integrate_part(f, start, end, n_iter, lock, result):
    """Функция для потока"""
    h = (end - start) / n_iter
    subtotal = sum(f(start + i*h) * h for i in range(n_iter))
    with lock:
        result[0] += subtotal

def integrate_parallel(f, a, b, n_iter=100000, n_threads=4):
    """Многопоточное интегрирование"""
    threads = []
    lock = threading.Lock()
    result = [0.0]

    chunk = (b - a) / n_threads
    iter_per_thread = n_iter // n_threads

    for i in range(n_threads):
        start = a + i*chunk
        end = start + chunk
        t = threading.Thread(target=integrate_part,
                             args=(f, start, end, iter_per_thread, lock, result))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return result[0]

print("Последовательное интегрирование:", integrate(math.sin, 0, 1, n_iter=100))
print("Последовательное интегрирование-2:", integrate2(math.cos, 0, 1, 100))
print("Параллельное интегрирование:", integrate_parallel(math.sin, 0, 1, n_iter=1000, n_threads=4))


# Измерение времени через timeit

n_iter_list = [10**4, 10**5, 10**6]

for n in n_iter_list:
    t_seq = timeit.timeit(
        f"integrate(math.sin, 0, 1, n_iter={n})",
        setup="from __main__ import integrate, math",
        number=10
    )
    t_seq2 = timeit.timeit(
        f"integrate2(math.sin, 0, 1, n_iter={n})",
        setup="from __main__ import integrate2, math",
        number=10
    )
    t_par = timeit.timeit(
        f"integrate_parallel(math.sin, 0, 1, n_iter={n}, n_threads=4)",
        setup="from __main__ import integrate_parallel, math",
        number=10
    )
    print(f"n_iter={n}: Интегрирование={t_seq:.4f}s, Интегрирование-2={t_seq2:.4f}s, Параллельное интегрирование={t_par:.4f}s")
