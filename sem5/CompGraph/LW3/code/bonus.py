import pygame
import random


class Bonus(pygame.sprite.Sprite):
    def __init__(self, ai_game, bonus_type):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # self.bonus_type = bonus_type  # Инициализация атрибута bonus_type

        # Загрузка изображения бонуса
        # Сердечки https://goblin-mode-games.itch.io/pixel-art-heart-capsules
        # Пузырьки https://verysmallsquares.itch.io/16

        self.image = pygame.image.load(f"resources/images/{bonus_type}_bonus.bmp")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.screen.get_width() - self.rect.width)
        self.rect.y = 0  # Бонус появляется сверху

        self.y = float(self.rect.y)

    def update(self):
        """Обновление позиции бонуса."""
        self.y += self.settings.bonus_speed  # Скорость падения бонуса
        self.rect.y = self.y

        # Печать информации о бонусе
        # self.print_bonus_info()

    def draw(self, screen):
        """Отображение бонуса на экране."""
        screen.blit(self.image, self.rect)

    # def print_bonus_info(self):
    #     """Печать информации о бонусе в консоль."""
    #     print(f"Bonus Type: {self.bonus_type}, Position: ({self.rect.x}, {self.rect.y})")
