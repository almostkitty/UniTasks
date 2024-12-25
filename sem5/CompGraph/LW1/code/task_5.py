import pygame
import numpy as np


pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Task 5")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (156, 124, 51)

L = np.array([[50, 100], [250, 200], [50, 200], [250, 300]])  
T = np.array([[1, 2], [3, 1]])        
transformed_L = np.dot(T, L.T).T

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)


    pygame.draw.line(screen, RED, L[0], L[1], 3)
    pygame.draw.line(screen, RED, L[2], L[3], 3)
    pygame.draw.line(screen, GREEN, transformed_L[0], transformed_L[1], 3)
    pygame.draw.line(screen, GREEN, transformed_L[2], transformed_L[3], 3)

    pygame.display.flip()


pygame.quit()