import pygame


pygame.init()

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Task 2")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (156, 124, 51)


font = pygame.font.SysFont('Arial', 36)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # Окружность
    pygame.draw.circle(screen, RED, (300, 150), 30)

    # Линия
    pygame.draw.line(screen, GREEN, (50, 400), (450, 400), 5)

    # Прямоугольник
    pygame.draw.rect(screen, BLUE, (100, 200, 300, 100))

    # Текст
    text = font.render("Какой-то текст", True, BROWN)
    screen.blit(text, (150, 50))

    pygame.display.flip()

pygame.quit()
