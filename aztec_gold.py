"""
A visualization of the Arctic Circle Theorem, idea from:
   https://www.youtube.com/watch?v=Yy7Q8IWNfHM (The ARCTIC CIRCLE THEOREM or Why do physicists play dominoes?)
"""
import numpy as np
import pygame

N, E, S, W = 1, 2, 3, 4
COLORS = np.array([
    [244, 241, 222],
    [224, 122, 95],
    [61, 64, 91],
    [129, 178, 154],
    [242, 204, 143],
])

def remove_collisions(tiles):
    up_down = (tiles[:-1] == S) & (tiles[1:] == N)
    left_right = (tiles[:, :-1] == E) & (tiles[:, 1:] == W)

    tiles[:-1][up_down] = 0
    tiles[1:][up_down] = 0
    tiles[:, :-1][left_right] = 0
    tiles[:, 1:][left_right] = 0

def dance(tiles):
    d, _ = tiles.shape
    new_tiles = np.zeros((d + 2, d + 2), dtype=np.uint8)

    new_tiles[:-2, 1: -1][tiles == N] = N
    new_tiles[2: , 1: -1][tiles == S] = S
    new_tiles[1: -1, :-2][tiles == W] = W
    new_tiles[1: -1, 2: ][tiles == E] = E
    return new_tiles

def fill(tiles):
    d, _ = tiles.shape
    half = d // 2
    offset = half - .5

    for y, x in np.argwhere(tiles == 0):
        if half < abs(y - offset) + abs(x - offset):
            continue
        if tiles[y, x] == 0:
            if round(np.random.random()):
                tiles[y, x: x + 2] = N
                tiles[y + 1, x: x + 2] = S
            else:
                tiles[y: y + 2, x] = W
                tiles[y: y + 2, x + 1] = E

def draw(screen, tiles):
    screen.fill(COLORS[0])
    surface = pygame.surfarray.make_surface(COLORS[tiles])
    surface = pygame.transform.scale(surface, (800, 800))
    screen.blit(surface, (0, 0))
    pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))

    tiles = np.zeros((2, 2), dtype=np.uint8)
    fill(tiles)
    draw(screen, tiles)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                remove_collisions(tiles)
                tiles = dance(tiles)
                fill(tiles)
                draw(screen, tiles)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                tiles = np.zeros((2, 2), dtype=np.uint8)
                fill(tiles)
                draw(screen, tiles)

if __name__ == "__main__":
    main()
