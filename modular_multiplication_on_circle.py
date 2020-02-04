"""
Pygame implementation of https://www.youtube.com/watch?v=qhbuKbxJsk8

Use up/down to change number of points and left/right to change the multiplication factor
"""
from collections import defaultdict
import numpy as np
import pygame

#Modify these as you will
DIM = 800
FORECOLOR = 193, 169, 13
BACKCOLOR = 17, 107, 156

#But Leave these alone
DIM_ARRAY = np.array([DIM, DIM])
CENTER = DIM_ARRAY / 2
RADIUS = DIM / 2 - 10
BLACK = 0, 0, 0
NUMBER_OF_POINTS = 40
FACTOR = 10

keys = defaultdict(bool)

pygame.init()

window = pygame.display.set_mode(DIM_ARRAY)
font = pygame.font.Font(pygame.font.get_default_font(), 20)
running = True

def coordinates(point):
    theta = point * 2 * np.pi / NUMBER_OF_POINTS
    return RADIUS * np.array([np.sin(theta), np.cos(theta)]) + CENTER

while running:

    window.fill(BACKCOLOR)
    for point in range(NUMBER_OF_POINTS):
        pygame.draw.aaline(window, FORECOLOR, coordinates(point), coordinates(FACTOR * point), 1)
    #Separate loop so lines don't draw on top of circles
    for point in range(NUMBER_OF_POINTS):
        pygame.draw.circle(window, BLACK, coordinates(point).astype(int), 4, 4)
    text_surfaces = [font.render(text, True, FORECOLOR)
                     for text in [f'Points: {NUMBER_OF_POINTS}', f'Factor: {round(FACTOR, 1)}']]
    window.blit(text_surfaces[0], dest=(10, 10))
    window.blit(text_surfaces[1], dest=(10, 30))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            keys[event.key] = True
        elif event.type == pygame.KEYUP:
            keys[event.key] = False

    if keys[pygame.K_UP]:
        NUMBER_OF_POINTS += 1
    if keys[pygame.K_DOWN]:
        NUMBER_OF_POINTS -= 1 if NUMBER_OF_POINTS else 0
    if keys[pygame.K_LEFT]:
        FACTOR -= .1
    if keys[pygame.K_RIGHT]:
        FACTOR += .1

pygame.quit()
