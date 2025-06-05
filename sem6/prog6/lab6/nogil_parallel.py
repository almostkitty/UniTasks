# nogil_parallel.py
import time
import os
import concurrent.futures as cf
import matplotlib.pyplot as plt
from cy_fermat_nogil import fermat_factorization_nogil as cy_fact_nogil
from ferma_fact import fermat_factorization as py_fact  # Обычная Python-функция


TEST_LST = [101, 9973, 104729, 101909, 609133, 1300039, 9999991,
            99999959, 99999971, 3000009, 700000133]

workers = os.cpu_count() or 4

def run_parallel(func, data, mode='thread', workers=4):
    Executor = cf.ThreadPoolExecutor if mode == 'thread' else cf.ProcessPoolExecutor
    with Executor(max_workers=workers) as executor:
        futures = [executor.submit(func, n) for n in data]
        results = [f.result() for f in futures]
    return results

def benchmark(func, data, mode, workers=4, repeat=3):
    times = []
    for _ in range(repeat):
        start = time.time()
        run_parallel(func, data, mode, workers)
        times.append(time.time() - start)
    return times

if __name__ == '__main__':
    print("Запуск многопоточного решения с освобождением GIL (Cython с nogil)")

    # Замер с потоками
    time_threads_cy = benchmark(cy_fact_nogil, TEST_LST, mode='thread', workers=workers)
    # Замер с процессами
    time_process_cy = benchmark(cy_fact_nogil, TEST_LST, mode='process', workers=workers)

    # Замер с потоками (Python)
    time_threads_py = benchmark(py_fact, TEST_LST, mode='thread', workers=workers)
    # Замер с процессами (Python)
    time_process_py = benchmark(py_fact, TEST_LST, mode='process', workers=workers)

    print(f"Cython nogil, потоки: {time_threads_cy}")
    print(f"Cython nogil, процессы: {time_process_cy}")
    print(f"Python, потоки: {time_threads_py}")
    print(f"Python, процессы: {time_process_py}")

    labels = ['Cython потоки', 'Cython процессы', 'Python потоки', 'Python процессы']
    means = [sum(time_threads_cy)/len(time_threads_cy),
             sum(time_process_cy)/len(time_process_cy),
             sum(time_threads_py)/len(time_threads_py),
             sum(time_process_py)/len(time_process_py)]

    plt.bar(labels, means)
    plt.ylabel('Среднее время выполнения (сек)')
    plt.title('Сравнение времени выполнения с многопоточностью и многопроцессностью')
    plt.xticks(rotation=15)
    for i, v in enumerate(means):
        plt.text(i, v + 0.01, f"{v:.3f}", ha='center', va='bottom')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('test_3.png', dpi=300)
