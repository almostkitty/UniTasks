import timeit
import time
import os
import matplotlib.pyplot as plt
from cy_fermat import fermat_factorization as cy_fact
from ferma_fact import fermat_factorization as py_fact
import concurrent.futures as cf


TEST_LST = [101, 9973, 104729, 101909, 609133, 1300039, 9999991,
            99999959, 99999971, 3000009, 700000133]


workers = os.cpu_count() or 4  # 4 - дефолтное

def run_parallel(func, data, workers, mode='thread'):
    if mode == 'thread':
        Executor = cf.ThreadPoolExecutor
    elif mode == 'process':
        Executor = cf.ProcessPoolExecutor
    else:
        raise ValueError("Аргумент 'thread' или 'process'")
    
    with Executor(max_workers=workers) as executor:
        start = time.time()
        list(executor.map(func, data))
        duration = time.time() - start
    return duration

def plot_baseline():
    print("Шаг 1: Замер времени обычной и Cython-реализаций")
    time_cy = timeit.repeat(
        "res = [fermat_factorization(i) for i in TEST_LST]",
        setup='from cy_fermat import fermat_factorization\n'
              'TEST_LST = [101, 9973, 104729, 101909, 609133, 1300039, '
              '9999991, 99999959, 99999971, 3000009, 700000133]',
        number=2,
        repeat=3
    )

    time_py = timeit.repeat(
        "res = [fermat_factorization(i) for i in TEST_LST]",
        setup='from ferma_fact import fermat_factorization\n'
              'TEST_LST = [101, 9973, 104729, 101909, 609133, 1300039, '
              '9999991, 99999959, 99999971, 3000009, 700000133]',
        number=2,
        repeat=3
    )

    print("Cython время:", time_cy)
    print("Python время:", time_py)

    mean_cy = sum(time_cy) / len(time_cy)
    mean_py = sum(time_py) / len(time_py)

    bars = plt.bar(['Python', 'Cython'], [mean_py, mean_cy])
    plt.title('Сравнение времени выполнения: Python vs Cython')
    plt.ylabel('Время (сек)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height * 1.01,
                f'{height:.3f} с', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.savefig("test_1.png", dpi=300)

def plot_parallel():
    print("Шаг 2: Параллельные вычисления потоками и процессами")

    results = []

    t1 = run_parallel(cy_fact, TEST_LST, mode='thread', workers=workers)
    results.append(("Cython потоки", t1))

    t2 = run_parallel(cy_fact, TEST_LST, mode='process', workers=workers)
    results.append(("Cython процессы", t2))

    t3 = run_parallel(py_fact, TEST_LST, mode='thread', workers=workers)
    results.append(("Python потоки", t3))

    t4 = run_parallel(py_fact, TEST_LST, mode='process', workers=workers)
    results.append(("Python процессы", t4))

    labels = [label for label, _ in results]
    times = [t for _, t in results]

    plt.figure(figsize=(10, 5))
    bars = plt.bar(labels, times)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height * 1.01,
                 f'{height:.2f} с', ha='center', va='bottom')

    plt.title(f'Сравнение потоков и процессов (workers={workers})')
    plt.ylabel('Время выполнения (сек)')
    plt.xticks(rotation=15)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('test_2.png', dpi=300)

if __name__ == '__main__':
    plot_baseline()
    plot_parallel()