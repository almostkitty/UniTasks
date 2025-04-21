import math
import timeit
import matplotlib.pyplot as plt


"""
Время вычислений (Baseline)  = 229.25 секунд

Шаг 1. Оставив представленный ниже код, переписать функции для нахождения чисел с помощью Cython, 
запустить timeit с аналогичными параметрами и сравнить два варианта, построить график.
С помощью annotate=True сгенерируйте html (где визуализировано взаимодействие с Python-интерпретатором) и приложите его к отчету. 
"""

"""
Шаг 2. Создать механизм распределения вычислений так, чтобы массив данных для вычисления распределялся
на несколько "вычислителей" и каждый вычислитель считал свое /map-reduce

1. Определить параметры: количество вычислителей, их тип (поток, процесс) и распределить по
 соответствующим очередям какие значения какому вычислителю идут. 
2. Отправить по очереди значения и дождаться пока все вычислители закончат работу
3. Оценить работу программы с потоками и процессами
"""

def is_perfect_square(n):
    """Проверяет, является ли число полным квадратом."""
    root = int(math.isqrt(n))
    return root * root == n


def fermat_factorization(N):
    """Разложение числа N на множители методом Ферма."""
    if N % 2 == 0:
        return 2, N // 2  # Если N четное, делим на 2

    x = math.isqrt(N) + 1  # Начинаем с ближайшего целого числа к √N
    while True:
        y_squared = x * x - N
        if is_perfect_square(y_squared):
            y = int(math.isqrt(y_squared))
            return (x - y, x + y)  # Возвращаем найденные множители
        x += 1  # Увеличиваем x


# Пример использования
if __name__ == '__main__':
    TEST_LST = [101, 9973, 104729, 101909, 609133, 1300039, 9999991, 99999959, 99999971, 3000009,
                700000133]

    time_cy = timeit.repeat("res = [fermat_factorization(i) for i in TEST_LST]",
                  setup='from cy_fermat import fermat_factorization\n'
                  'TEST_LST = [101, 9973, 104729, 101909, 609133, 1300039, '
                  '9999991, 99999959, 99999971, 3000009, 700000133]',
                  number=10, repeat=5)
    
    print("Cython время:", time_cy)

    time_py = timeit.repeat("res = [fermat_factorization(i) for i in TEST_LST]",
                  setup='from main import fermat_factorization\n'
                  'TEST_LST = [101, 9973, 104729, 101909, 609133, 1300039, '
                  '9999991, 99999959, 99999971, 3000009, 700000133]',
                  number=10, repeat=5)

    print("Python время:", time_py)


    plt.figure(figsize=(12, 6))
    plt.plot(range(1, len(time_cy) + 1), time_cy, label='Cython', marker='o', color='b')
    plt.plot(range(1, len(time_py) + 1), time_py, label='Python', marker='x', color='r')

    plt.title('Python vs Cython')
    plt.xlabel('Повтор')
    plt.ylabel('Время выполнения, сек.')
    plt.legend()
    plt.grid(True)

    plt.savefig('1.png', dpi=300)