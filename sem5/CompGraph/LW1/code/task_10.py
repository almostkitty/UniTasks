import pygame
import numpy as np


pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Task 10")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

a = 30
b = 100
angle = 6 * np.pi
center = (250, 250)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    for theta in np.linspace(0, angle, 5000):

        # Расчет радиуса по формуле улитки Паскаля
        r = b + 2 * a * np.cos(theta)
        # Перевод из полярных координат в декартовы
        x = int(center[0] + r * np.cos(theta))
        y = int(center[1] + r * np.sin(theta))

        pygame.draw.circle(screen, RED, (x, y), 1)

    pygame.display.flip()

pygame.quit()
