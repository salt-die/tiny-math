"""
Permutations as objects that one can multiply.

Example:
    >>> p = Permutation(1, 2, 0, 3, 4)

    >>> q = Permutation(3, 1, 2, 0, 4)

    >>> p * q
    Permutation(3, 2, 0, 1, 4)

    >>> q * p
    Permutation(1, 2, 3, 0, 4)
"""


class Permutation:
    def __init__(self, *seq):
        if not all(i in seq for i in range(len(seq))):
            raise ValueError("Not a proper permutation.")
        self.seq = seq

    def __mul__(self, other):
        if not isinstance(other, Permutation):
            raise TypeError("Not a permutation.")

        if not len(other) == len(self):
            raise ValueError("Length mismatch.")

        return Permutation(*(self.seq[i] for i in other.seq))

    def __len__(self):
        return len(self.seq)

    def __repr__(self):
        return f"Permutation({', '.join(str(i) for i in self.seq)})"
