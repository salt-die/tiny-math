"""
Two python implementations of a surreal number.  The first implementation tries to stick as close to the original
definition as we can -- L and R are collections of numbers.  For the second we just use max(L) and min(R) when adding
or multiplying to keep generated numbers a bit simpler.
"""
from itertools import chain, product, starmap
from operator import add, neg
from functools import partial


def stringify(iterable):
    return ', '.join(str(member) for member in iterable)

def maybe_comma(iterable):
    return "," if len(iterable) == 1 else ""


class Number:
    """
    Note we use tuples for L and R instead of sets since `Number`s aren't hashable. Even if we defined a __hash__ it
    would do little to remove duplicate Numbers from the sets, so tuples it is.
    """
    def __init__(self, L=(), R=(), *, name=None):
        self.L = tuple(sorted(L))
        self.R = tuple(sorted(R))
        self.name = name

        for l, r in product(self.L, self.R):
            assert l <= r

    def __repr__(self):
        return f'Number(L=({stringify(self.L)}{maybe_comma(self.L)}), R=({stringify(self.R)}{maybe_comma(self.R)}))'

    def __str__(self):
        if self.name is not None: return self.name
        return f'{{{stringify(self.L)}|{stringify(self.R)}}}'

    def __ge__(self, other):
        return not (any(member <= other for member in self.R) or any(self <= member for member in other.L))

    def __le__(self, other): return other >= self

    def __eq__(self, other): return self >= other and other >= self

    def __gt__(self, other): return self >= other and not other >= self

    def __lt__(self, other): return other > self

    def __add__(self, other):
        left = chain(map(other.__add__, self.L), map(self.__add__, other.L))
        right = chain(map(other.__add__, self.R), map(self.__add__, other.R))
        return Number(left, right)

    def __neg__(self): return Number(map(neg, self.R), map(neg, self.L))

    def __sub__(self, other): return self + (-other)

    def __mul__(self, other):
        def times(x, y): return x * other + self * y - x * y

        left = chain(starmap(times, product(self.L, other.L)), starmap(times, product(self.R, other.R)))
        right = chain(starmap(times, product(self.R, other.L)), starmap(times, product(self.L, other.R)))
        return Number(left, right)

    def simplify(self):
        """Return the equivalent number with `L=max(self.L)` and `R=min(self.R).`"""
        left = (max(self.L).simplify(),) if self.L else ()
        right = (min(self.R).simplify(),) if self.R else ()
        return Number(left, right, name=self.name)


def comp(x, y):
    if x is None: return y
    if y is None: return x
    return max(x, y)


class FiniteNumber:
    """
    `FiniteNumber`s only keep max(L) and min(R).  This should speed up the lot of combinatoric comparisons.
    Unfortunately, this method ruins a bit of the original elegance since we need special checks if R is None or L is
    None.

    Even taking care to keep a single `FiniteNumber` in L and R, combinatorial explosion can still happen quite rapidly.
    """
    def __init__(self, L=None, R=None, name=None):
        self.L = L
        self.R = R
        self.name = name

    def __repr__(self):
        return f'FiniteNumber(L={str(self.L) if self.L else ""}, R={str(self.R) if self.R else ""})'

    def __str__(self):
        if self.name is not None: return self.name
        return f'{{{self.L if self.L else ""}|{self.R if self.R else ""}}}'

    def __ge__(self, other):
        return not (self.R and self.R <= other or other.L and self <= other.L)

    def __le__(self, other): return other >= self

    def __eq__(self, other): return self >= other and other >= self

    def __gt__(self, other): return self >= other and not other >= self

    def __lt__(self, other): return other > self

    def __add__(self, other):
        def add(x, y):
            if x is None or y is None: return None
            return x + y

        left = comp(add(other, self.L), add(self, other.L))
        right = comp(add(other, self.R), add(self, other.R))

        return FiniteNumber(left, right)

    def __neg__(self): return FiniteNumber(None if self.R is None else -self.R, None if self.L is None else -self.L)

    def __sub__(self, other): return self + (-other)

    def __mul__(self, other):
        def times(x, y):
            if x is None or y is None: return None
            return x * other + self * y - x * y

        left = comp(times(self.L, other.L), times(self.R, other.R))
        right = comp(times(self.R, other.L), times(self.L, other.R))
        return FiniteNumber(left, right)


if __name__ == '__main__':
    zero = FiniteNumber(name='0')
    one = FiniteNumber(L=zero, name='1')
    minus_one = FiniteNumber(R=zero, name='-1')
    two = FiniteNumber(L=one, name='2')
    three = FiniteNumber(L=two, name='3')
    print('1 + 1 == 2:', one + one == two)
    print('1 + 1 + 1 == 3:', one + one + one == three)
    print('0 * 1 == 0 * 2:', zero * one == zero * two)
    print('1 + -1 == 0:', one + minus_one == zero)
    print('2 * 3 == 3 + 3:', two * three == three + three)
    print('3 + 3 > 3 + 2:', three + three > three + two)