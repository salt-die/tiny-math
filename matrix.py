"""
Pure Python matrix implementation.
"""
from collections.abc import Iterable
from numbers import Real


class Matrix:
    def __init__(self, rows: Iterable[list[Real]]):
        self._rows = [list(row) for row in rows]

    def __repr__(self):
        return f"{type(self).__name__}({self._rows})"

    def __iter__(self):
        yield from self._rows

    def __len__(self):
        h, w = self.shape
        return h * w

    def __getitem__(self, item):
        match item:
            case int():
                return self._rows[item].copy()
            case slice():
                rows = self._rows[item]
                return type(self)(rows)
            case slice() as i, int() as j:
                rows = self._rows[i]
                return [row[j] for row in rows]
            case slice() as i, slice() as j:
                rows = self._rows[i]
                return type(self)(row[j] for row in rows)
            case int() as i, int() as j:
                return self._rows[i][j]

        raise IndexError("bad index format")

    def __setitem__(self, item, value):
        match item:
            case int() | slice():
                self._rows[item] = value
                self._rows[item] = value
            case slice() as i, int() | slice() as j:
                for col in self._rows[i]:
                    col[j] = value

            case int() as i, int() as j:
                self._rows[i][j] = value
            case _:
                raise IndexError("bad index format")

    def __matmul__(self, other):
        _, w = self.shape
        h, _ = other.shape

        if w != h:
            raise ValueError("matrices not compatible")

        otherT = other.T

        return type(self)(
            [
                sum(a * b for a, b in zip(row, col))
                for col in otherT
            ]
            for row in self
        )

    @property
    def T(self):
        """
        Transpose of matrix.
        """
        _, w = self.shape
        return type(self)(self[:, i] for i in range(w))

    @property
    def shape(self):
        if not self._rows:
            return 0, 0

        return len(self._rows), len(self._rows[0])

    def minor(self, i, j):
        return type(self)(
            [e for m, e in enumerate(row) if m != j]
            for n, row in enumerate(self) if n != i
        )

    def cofactor(self, i, j):
        return (-1)**(i + j) * self.minor(i, j).determinant()

    def determinant(self):
        cols, rows = self.shape
        if cols != rows:
            raise ValueError("not a square matrix")

        if cols == 1:
            return self._rows[0][0]

        return sum(e * self.cofactor(0, j) for j, e in enumerate(self[0]))
