# cy_fermat_nogil.pyx
from libc.math cimport sqrt

cdef long long isqrt(long long n) nogil:
    cdef long long x, y
    if n == 0:
        return 0
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

cdef bint is_perfect_square_c(long long n) nogil:
    cdef long long root = isqrt(n)
    return root * root == n

cdef void fermat_factorization_c(long long N, long long* a, long long* b) nogil:
    cdef long long x, y_squared, y
    if N % 2 == 0:
        a[0] = 2
        b[0] = N // 2
        return
    x = isqrt(N) + 1
    while True:
        y_squared = x * x - N
        if is_perfect_square_c(y_squared):
            y = isqrt(y_squared)
            a[0] = x - y
            b[0] = x + y
            return
        x += 1

cpdef tuple fermat_factorization_nogil(long long N):
    cdef long long a = 0
    cdef long long b = 0
    with nogil:
        fermat_factorization_c(N, &a, &b)
    return (a, b)
