import math

def is_perfect_square(n):
    """Проверяет, является ли число полным квадратом."""
    root = int(math.isqrt(n))
    return root * root == n

def fermat_factorization(N):
    """Разложение числа N на множители методом Ферма."""
    if N % 2 == 0:
        return (2, N // 2)
    
    x = math.isqrt(N) + 1
    while True:
        y_squared = x * x - N
        if is_perfect_square(y_squared):
            y = int(math.isqrt(y_squared))
            return (x - y, x + y)
        x += 1
