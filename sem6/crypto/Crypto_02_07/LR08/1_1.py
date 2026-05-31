from math import gcd
from sympy import factorint, mod_inverse

alphabet = [
    " ", "а", "б", "в", "г", "д", "е", "ж", "з", "и",
    "й", "к", "л", "м", "н", "о", "п", "р", "с", "т",
    "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь",
    "э", "ю", "я"
]

def decode_block(block_str):
    result = ""
    for j in range(0, len(block_str), 2):
        code = int(block_str[j:j+2])
        if 0 <= code <= 32:
            result += alphabet[code]
        else:
            result += "?"
    return result

m = 3273550829
E = 1925928379
cipher_blocks = [
    1169117912, 1244629799, 2168855069, 1243855092, 437023454,
    2762017513, 127848283, 47229456, 2567946795, 2860789969,
    3245731988, 34676752, 1557331563, 1308187811
]

# Шаг 1: Факторизация m
print("[1] Факторизация m:")
factors = factorint(m)
print(f"m = {m}")
print(f"Факторы: {factors}")

# Извлекаем p и q
if len(factors) != 2:
    raise ValueError("m не является произведением двух простых — RSA не работает.")
p, q = list(factors.keys())
print(f"p = {p}, q = {q}")

# Шаг 2: Вычисляем phi(n)
phi = (p - 1) * (q - 1)
print(f"\n[2] Вычисление phi(n):")
print(f"phi(n) = (p - 1) * (q - 1) = {phi}")

# Шаг 3: Находим D — обратный элемент к E по модулю φ(n)
D = mod_inverse(E, phi)
print(f"\n[3] Вычисление D:")
print(f"D = E^(-1) mod phi(n) = {D}")

# Шаг 4: Расшифровка блоков
print(f"\n[4] Расшифровка блоков:")
decoded_message = ""
for i, c in enumerate(cipher_blocks):
    m_plain = pow(c, D, m)
    block_str = str(m_plain).zfill(10)  # блок длиной 10 цифр
    print(f"    Блок {i+1:>2}: C = {c}")
    print(f"            M = C^D mod m = {m_plain} -> '{block_str}'")

    decoded = decode_block(block_str)
    print(f"Декодировано: '{decoded}'")
    decoded_message += decoded

# Шаг 5: Вывод финального сообщения
print(f"\n[5] Итоговое сообщение:")
print(decoded_message)
