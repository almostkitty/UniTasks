import pygame
import numpy as np


pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Task 4")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (156, 124, 51)

L = np.array([[0, 100], [200, 300]])  
T = np.array([[1, 2], [3, 1]])        
transformed_L = (T @ L.T).T

mid_L = (L[0] + L[1]) / 2
mid_trans_L = (transformed_L[0] + transformed_L[1]) / 2

# Уменьшение в 2 раза, чтобы поместилось в границы окна
scale = 0.5
scaled_L = L * scale
scaled_transformed_L = transformed_L * scale
scaled_mid_L = mid_L * scale
scaled_mid_transformed_L = mid_trans_L * scale


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)


    pygame.draw.line(screen, RED, scaled_L[0], scaled_L[1], 2)
    pygame.draw.circle(screen, RED, scaled_mid_L.astype(int), 3)

    pygame.draw.line(screen, GREEN, scaled_transformed_L[0], scaled_transformed_L[1], 2)
    pygame.draw.circle(screen, GREEN, scaled_mid_transformed_L.astype(int), 3)

    pygame.draw.line(screen, BLUE, scaled_mid_L, scaled_mid_transformed_L, 1)

    pygame.display.flip()


pygame.quit()