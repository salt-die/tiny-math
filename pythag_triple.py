"""
Generate an arbitrary pythagorean triple with gen_triple.  n must be an integer.
"""

from sympy import factorint
from collections import Counter
from random import randint, shuffle
from math import prod

def random_factoring(n): # Finds a factoring of n**2/2
    factors = factorint(n)
    factors = Counter(factors)

    factors = list(factors.elements()) * 2 # n**2
    factors.remove(2)                      # n/2

    shuffle(factors)
    split = randint(1, len(factors))
    return prod(factors[:split]), prod(factors[split:])

def gen_triple(n):
    r = 2 * n
    s, t = random_factoring(r)
    return r + s, r + t, r + s + t
