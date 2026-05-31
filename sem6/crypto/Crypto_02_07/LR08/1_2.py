from sympy import factorint, mod_inverse
import time

c = 31562390514325508322912233641018233293067940145944
e = 3
m = 72345504624922694803343276405691785887459968779467

# Шаг 1: Факторизация m
start_time = time.time()
factors = factorint(m)
end_time = time.time()
print(f"Факторы числа m: {factors}")
print(f"Время факторизации: {end_time - start_time:.5f} секунд")

# p и q
if len(factors) != 2:
    raise ValueError("m не является произведением двух простых чисел — RSA не сработает.")
p, q = list(factors.keys())
print(f"p = {p}, q = {q}")

# Шаг 2: Вычисление phi(m)
phi_m = (p - 1) * (q - 1)
print(f"φ(m) = (p - 1) * (q - 1) = {phi_m}")

# Шаг 3: Вычисление d
d = mod_inverse(e, phi_m)
print(f"Закрытый ключ d = {d}")

# Шаг 4: Расшифровка
decrypted_message = pow(c, d, m)
print(f"Расшифрованное сообщение (в виде числа): {decrypted_message}")

# Преобразование числа в строку
decoded_message = str(decrypted_message)
print(f"Расшифрованное сообщение (в строковом виде): {decoded_message}")
end_time = time.time()
print(f"Общее время расшифровки: {end_time - start_time:.5f} секунд")
