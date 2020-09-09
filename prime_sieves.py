import numpy as np

def primes_from_2_to(n):
    sieve = np.ones(n//3 + (n % 6 == 2), dtype=np.bool)

    for i in range(1, int(n**.5)//3 + 1):
        if sieve[i]:
            k= 3 * i + 1 | 1
            sieve[           k * k//3          :: 2 * k] = False
            sieve[k * (k - 2 * (i & 1) + 4)//3 :: 2 * k] = False
    return np.r_[2, 3, 3 * np.nonzero(sieve)[0][1:] + 1 | 1]


def primes_to_(n):
    ints = [True] * (n + 1)

    ints[0:2] = [False, False]
    ints[4::2] = [False] * ((n - 4) // 2 + 1)

    for i in range(3, int(n**.5) + 1, 2):
        if ints[i]:
            ints[i**2::i] = [False] * ((n - i**2) // i + 1)

    return [i for i, is_prime in enumerate(ints) if is_prime]