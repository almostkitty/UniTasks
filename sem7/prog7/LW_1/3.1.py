import math
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed


def integrate_chunk(f, start, end, n_iter):
    h = (end - start) / n_iter
    return sum(f(start + i*h) * h for i in range(n_iter))

def integrate(f, a, b, *, n_iter=10**6, n_workers=4, executor_type='thread'):
    chunk = (b - a) / n_workers
    iter_per_worker = n_iter // n_workers
    futures = []
    results = []

    if executor_type == 'thread':
        Executor = ThreadPoolExecutor
    elif executor_type == 'process':
        Executor = ProcessPoolExecutor
    else:
        raise ValueError("executor_type должен быть 'thread' или 'process'")

    with Executor(max_workers=n_workers) as executor:
        for i in range(n_workers):
            start = a + i*chunk
            end = start + chunk if i < n_workers-1 else b
            futures.append(executor.submit(integrate_chunk, f, start, end, iter_per_worker))

        for future in as_completed(futures):
            results.append(future.result())

    return sum(results)

# Замеры времени через timeit
if __name__ == "__main__":
    import timeit

    repeat = 100
    n_iter = 10**6
    worker_list = [2, 4, 6]

    for n_workers in worker_list:
        t_thread = timeit.timeit(
            stmt=f"integrate(math.atan, 0, math.pi/2, n_iter={n_iter}, n_workers={n_workers}, executor_type='thread')",
            setup="from __main__ import integrate, math",
            number=1
        )
        t_process = timeit.timeit(
            stmt=f"integrate(math.atan, 0, math.pi/2, n_iter={n_iter}, n_workers={n_workers}, executor_type='process')",
            setup="from __main__ import integrate, math",
            number=1
        )
        print(f"{n_workers} потоков: {t_thread*1000:.2f} мсек, {n_workers} процессов: {t_process*1000:.2f} мсек")
