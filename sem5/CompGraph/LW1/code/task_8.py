import pygame
import numpy as np


pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Task 8")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (156, 124, 51)

TRIANGLE = np.array([[8, 1], [7, 3], [6, 2]]) * 33
T = np.array([[0, 1], [1, 0]])  
R_TRIANGLE = (T @ TRIANGLE.T).T + np.array([210, 220])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    pygame.draw.polygon(screen, RED, TRIANGLE + [210, 220], 2)  
    pygame.draw.polygon(screen, BLUE, R_TRIANGLE, 2)

    pygame.display.flip()


pygame.quit()