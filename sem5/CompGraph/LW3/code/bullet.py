import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_game, enhanced=False):
        super().__init__()
        self.screen = ai_game.screen
        self.color = ai_game.settings.bullet_color
        self.speed = ai_game.settings.bullet_speed

        self.rect = pygame.Rect(0, 0, ai_game.settings.bullet_width, ai_game.settings.bullet_height)

        # Если снаряд усиленный, увеличиваем длину
        if enhanced:
            self.rect.height *= 10


        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

        self.enhanced = enhanced  # Флаг, указывающий, усиленный ли снаряд


    def update(self):
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)