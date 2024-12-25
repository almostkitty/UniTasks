import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """Класс для управления кораблем."""

    def __init__(self, ai_game):
        """Инициализирует корабль и задает его начальную ползицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Загружает изображение корабля и получает прямоугольник.
        # https://opengameart.org/content/spaceships-32x32 - спрайты корабля
        self.image = pygame.image.load('resources/images/ship_5.bmp')
        self.rect = self.image.get_rect()
        # Каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom
        # Сохранение вещественной координаты центра корабля.
        self.center = float(self.rect.centerx)
        # Флаг перемещения
        self.moving_right = False
        self.moving_left = False
        self.shield_active = False  # Добавляем флаг для щита
        self.power_active = False  # Флаг для усиленных снарядов

    def update(self):
        """Обновление позиции корабля."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.center -= self.settings.ship_speed

        self.rect.centerx = self.center

        # Если щит активен, игнорируем столкновения с инопланетянами
        if self.shield_active:
            self.image.set_alpha(128)  # Полупрозрачность для щита
        else:
            self.image.set_alpha(255)

    def activate_shield(self):
        """Активирует щит, который защищает корабль."""
        self.shield_active = True
        # Временная деактивация щита через некоторое время
        pygame.time.set_timer(pygame.USEREVENT, 5000)  # 5 секунд щита

    def deactivate_shield(self):
        """Деактивирует щит."""
        self.shield_active = False
        pygame.time.set_timer(pygame.USEREVENT, 0)  # Останавливаем таймер

    def activate_power(self):
        """Активирует усиленные снаряды."""
        self.power_active = True
        # Временная деактивация усиленных снарядов через некоторое время
        pygame.time.set_timer(pygame.USEREVENT + 1, 5000)  # 5 секунд усиленных снарядов

    def deactivate_power(self):
        """Деактивирует усиленные снаряды."""
        self.power_active = False
        pygame.time.set_timer(pygame.USEREVENT + 1, 0) 

    def blitme(self):
        """Рисует корабль в текущей позиции."""
        self.screen.blit(self.image, self.rect)


    def center_ship(self):
        """Размещает корабль в центре нижней стороны."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)