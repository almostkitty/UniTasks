import random

n = random.randint(1, 100)
m = random.randint(1, 100)
b = random.randint(1, 100)

def rem(n, m, b):
    if m == 0:
        return 1
    if m % 2 == 0:
        return rem((n * n) % b, m // 2, b)
    else:
        return (n * rem((n * n) % b, (m - 1) // 2, b)) % b

result = rem(n, m, b)

print(f"При n = {n}, m = {m}, b = {b}, результат = {result}")
