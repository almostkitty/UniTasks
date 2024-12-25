import pygame
import numpy as np


pygame.init()

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Task 3")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

line_start = np.array([8, 17])
line_end = np.array([20, 32])

T = np.array([[1, 3], [4, 1]])

transformed_start = T @ line_start
transformed_end = T @ line_end

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    pygame.draw.line(screen, RED, line_start, line_end, 3)
    pygame.draw.line(screen, GREEN, transformed_start, transformed_end, 3)
    pygame.display.flip()

pygame.quit()