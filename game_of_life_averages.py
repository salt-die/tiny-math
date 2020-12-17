"""
Game of life, but newly born cells are the average color of their parents.

Press "r" to reset the universe, click to draw.
"""
import numpy as np
import scipy.ndimage as nd
import pygame

KERNEL = np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1]], dtype=np.uint8)
DIM = 500, 500
window = pygame.display.set_mode(DIM)

def main():
    universe = np.random.randint(2, size=DIM)
    RGB = [np.where(universe, np.random.randint(256, size=DIM), 0) for _ in range(3)]
    MOUSEDOWN = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # Reset
                universe = np.random.randint(2, size=DIM)
                RGB = [np.where(universe, np.random.randint(256, size=DIM), 0) for _ in range(3)]
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                MOUSEDOWN = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                MOUSEDOWN = False

        if MOUSEDOWN:
            row, column = pygame.mouse.get_pos()
            poke = slice(row - 2, row + 3), slice(column - 2, column + 3)
            # Draw new cells at cursor
            universe[poke] = 1
            for color in RGB:
                color[poke] = np.random.randint(256)

        # Update state
        neighbors = nd.convolve(universe, KERNEL, mode="constant")

        still_alive = universe & (neighbors > 1) & (neighbors < 4)
        new_borns = ~universe & (neighbors == 3)
        universe = still_alive + new_borns

        old_colors = [np.where(still_alive, color, 0) for color in RGB]
        new_colors = [np.where(new_borns, nd.convolve(color, KERNEL, mode="constant") / 3, 0) for color in RGB]

        RGB = [sum(color) for color in zip(old_colors, new_colors)]

        pygame.surfarray.blit_array(window, np.dstack(RGB))
        pygame.display.update()

pygame.init()
main()
pygame.quit()
