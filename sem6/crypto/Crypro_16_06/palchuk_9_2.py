def rem(n, m, b):
    if m == 0:
        return 1
    if m % 2 == 0:
        return rem((n * n) % b, m // 2, b)
    else:
        return (n * rem((n * n) % b, (m - 1) // 2, b)) % b

print(rem(12, 8, 17))
