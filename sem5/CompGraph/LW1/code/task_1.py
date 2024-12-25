import pygame
import numpy as np


pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Task 1")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

point = np.array([10, 20])  
T = np.array([[1, 3], [4, 1]])  


transformed_point = T @ point

point = point.astype(int)
transformed_point = transformed_point.astype(int)

print(f"Начальные координаты: {point}")
print(f"Полученные координаты: {transformed_point}")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # Тут целочисленные
    pygame.draw.circle(screen, RED, point, 5)
    pygame.draw.circle(screen, GREEN, transformed_point, 5)

    pygame.display.flip()

pygame.quit()