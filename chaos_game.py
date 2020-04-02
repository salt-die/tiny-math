from random import choice
import numpy as np

PHI = (1 + 5**.5) / 2


def make_base(n=3):
    base = []
    arc = 2 * np.pi / n
    for i in range(n):
        theta = i * arc
        base.append([np.sin(theta), np.cos(theta)])
    return base


def chaos_game(point=np.array([1, 1]), force_new_corner=False, niter=10000, base_points=3, ratio=.5):
    previous = None
    xs, ys = [], []
    base = make_base(base_points)

    for _ in range(niter):
        if force_new_corner:
            while True:
                corner = choice(base)
                if corner != previous:
                    break
            previous = corner
        else:
            corner = choice(base)

        point = x, y = point - (point - corner) * ratio
        xs.append(x)
        ys.append(y)

    plt.scatter(xs, ys, s=1)
    plt.show()


if __name__ == "__main__":
    chaos_game()
    chaos_game(base_points=5, ratio=1/PHI)
