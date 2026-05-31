import math

a = 42

z1 = (0.5 + 0.5 * math.sqrt(-3 + 4 * a**2)) / a
z2 = (0.5 - 0.5 * math.sqrt(-3 + 4 * a**2)) / a
z3 = (1 + math.sqrt(1 + 4 * a**2)) / 2*a
z4 = (-1 + math.sqrt(1 + 4 * a**2)) / 2*a

roots = [z1, z2, z3, z4]
positive_roots = [z for z in roots if z > 0]
min_root = min(positive_roots)
password = str(min_root).replace('.', '')[:6]

print("Roots:", roots)
print("Positive roots:", positive_roots)
print("Min positive roots:", min_root)
print("Password:", password)
