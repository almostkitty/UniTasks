import random

# 1. Бинарный алгоритм возведения в степень по модулю (Для aˆx mod m)
def bin_pow(a, x, m):
    result = 1
    a = a % m

    while x > 0:
        if x & 1:
            result = (result * a) % m
        a = (a * a) % m
        x >>= 1

    return result


a = random.randint(1, 10**5)
x = random.randint(1, 10**5)
m = random.randint(1, 10**5)

print(f"({a} ** {x}) % {m} =", bin_pow(a, x, m))

# 2. Итеративный алгоритм Евклида (Для поиска gcd(a,b))
def gcd(c, b):
    while b != 0:
        c, b = b, c % b
    return c

print((lambda x, y: f"Для чисел {x} и {y} gcd равен {gcd(x, y)}")(random.randint(1, 10**5), random.randint(1, 10**5)))

# 3.Вычисление мультипликативно обратного
# Расширенный алгоритм Евклида для поиска gcd и коэффициентов
def euc(a, b):
    if b == 0:
        return a, 1, 0
    else:
        k, x1, y1 = euc(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return k, x, y

# Поиск мультипликативного обратного числа a по модулю m (a^(-1) mod m)
def mod_inv(a, m):
    k, x, _ = euc(a, m) # y игнорирую
    if k != 1:
        return None
    else:
        return x % m


a_inv = random.randint(1, 10**5)
m_inv = random.randint(1, 10**5)

inv = mod_inv(a_inv, m_inv)

if inv is None:
    print(f"Обратного числа к {a_inv} по модулю {m_inv} не существует (числа не взаимно просты).")
else:
    print(f"Обратное число к {a_inv} по модулю {m_inv} равно {inv}")
    print(f"Проверка: ({a_inv} * {inv}) % {m_inv} = {(a_inv * inv) % m_inv}")
