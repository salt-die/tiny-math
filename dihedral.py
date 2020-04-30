"""Rotate and reflect polygons with `*` and `~`!"""

from collections import deque
import numpy as np

τ = 2 * np.pi  # tau

one =   ['   ',
         '  |',
         '  |']
two =   [' _ ',
         ' _|',
         '|_ ']
three = [' _ ',
         ' _|',
         ' _|']
four =  ['   ',
         '|_|',
         '  |']
five =  [' _ ',
         '|_ ',
         ' _|']
six =   [' _ ',
         '|_ ',
         '|_|']
seven = ['__ ',
         '  |',
         '  |']
eight = [' _ ',
         '|_|',
         '|_|']
nine =  [' _ ',
         '|_|',
         '  |']
zero =  [' _ ',
         '| |',
         '|_|']
digits = one, two, three, four, five, six, seven, eight, nine, zero
digits = (list(map(list, digit)) for digit in digits)
translate = dict(zip('1234567890', digits))


class Ngon(tuple):
    def __new__(cls, n):
        if isinstance(n, int):
            return super().__new__(cls, range(n))
        else:
            return super().__new__(cls, n)

    def __repr__(self):
        return f'<{super().__repr__()[1:-1]}>'

    def __mul__(self, other):
        new_vertices = deque(self)
        new_vertices.rotate(other)
        return Ngon(new_vertices)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __invert__(self):
        new_vertices = deque(self)
        new_vertices.reverse()
        new_vertices.appendleft(new_vertices.pop())

        return Ngon(new_vertices)


class NgonVis(Ngon):
    """Same as Ngon, but with ascii art polygons."""
    def __repr__(self):
        return NgonPrinter.show(self)


class NgonPrinter:
    r = 12  # radius of our ngon

    @staticmethod
    def _set_points(n):
        """Returns the points of a ngon; points2 is just points shifted by 1"""
        r = NgonPrinter.r
        points = [(.95 * r * np.cos(τ * i / n), .95 * r * np.sin(τ * i / n)) for i in range(n)]
        points2 = points[1:] + [points[0]]
        return points, points2

    @classmethod
    def _line_segment(cls, x1, y1, x2, y2, grid, value='*'):
        """Draw a line segment from (x1, y1) to (x2, y2)."""
        # first we int-ify segment coordinates and make sure (0, 0) is center of our grid
        x1, y1, x2, y2 = (int(i) - cls.r for i in (x1, -y1, x2, -y2))

        angle = np.arctan2(y2 - y1, x2 - x1)              # angle of segment
        angle = np.array([np.sin(angle), np.cos(angle)])  # convert angle to a vector

        with np.errstate(divide="ignore"):
            delta = abs(1 / angle)

        step = np.sign(angle)
        grid_dis = np.where(step > 0, delta, 0)    # distance to next grid point if step is positive else 0

        # We'll start at map_pos and iteratively step to closest grid point and mark it with a '*' until we're close
        # enough to the end of the segment.
        map_pos = np.array([y1, x1])  # flipped coordinates because numpy indexing
        while True:
            if np.linalg.norm(map_pos - (y2, x2)) <= 1:  # if distance to end of segment <= 1
                break

            grid[tuple(map_pos)] = value  # mark current location

            side = int(grid_dis[0] > grid_dis[1])  # which integer coordinate is closest to us?
            grid_dis[side] += delta[side]          # increment that coordinate by delta
            map_pos[side] += step[side]            # step to that coordinate

    @classmethod
    def show(cls, ngon):
        grid = np.full((cls.r * 2 + 1, ) * 2, ' ')

        for p1, p2, vertex in zip(*cls._set_points(len(ngon)), ngon):
            cls._line_segment(*p1, *p2, grid)

            # translate vertex number into an ascii art array of characters
            vertex = np.array(list(zip(*map(translate.get, str(vertex))))).reshape(3, -1)
            x, y = (.5 * np.array(p1) + cls.r).astype(int)  # .5 to move the numbers a bit closer to the origin
            grid[y: y + vertex.shape[0], x: x + vertex.shape[1]] = vertex  # paste the digit into our grid

        return '\n'.join(' '.join(row) for row in grid)
