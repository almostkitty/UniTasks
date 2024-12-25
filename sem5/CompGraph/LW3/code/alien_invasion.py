import sys
from time import sleep
import pygame
import pickle
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from bonus import Bonus
import random


pygame.init()
pygame.mixer.init()

laser_sound = pygame.mixer.Sound("resources/sounds/peew.wav")
alien_explosion_sound = pygame.mixer.Sound("resources/sounds/ufo.wav")
life_lost_sound = pygame.mixer.Sound("resources/sounds/life.wav")
game_over_sound = pygame.mixer.Sound("resources/sounds/end.wav")

def save_game(data, filename="resources/saves/savefile.pkl"):
    """Сохраняет данные игры в файл."""
    with open(filename, "wb") as f:
        pickle.dump(data, f)
    print("Игра сохранена.")

def load_game(filename="resources/saves/savefile.pkl"):
    """Загружает данные игры из файла."""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("Файл сохранения не найден. Начинаем новую игру.")
        return None


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,  self.settings.screen_height))
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bonuses = pygame.sprite.Group()

        self.bonuses.update()


        self._create_fleet()
        self.play_button = Button(self, "Play")

        try:
            self.background_image = pygame.image.load(self.settings.background_image)
            self.settings.background_rect = self.background_image.get_rect()
        except pygame.error:
            print("Ошибка загрузки фонового изображения, будет использован стандартный цвет фона.")
            self.background_image = None

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        """Определяет количество рядов, помещающихся на экране."""
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        # Создание флота вторжения
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        if any(alien.check_edges() for alien in self.aliens.sprites()):
            self._change_fleet_direction()

    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_high_score(self):
        """Проверяет, является ли текущий результат новым рекордом."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.sb.prep_high_score()

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем."""
        if self.stats.ships_left > 0:
            # Уменьшение ships_left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Очистка списков пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()

            # Воспроизведение звука потери жизни
            life_lost_sound.play()

            #Пауза
            sleep(0.5)
        
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            # Звук проигрыша
            game_over_sound.play()

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

            # Отображение последнего прорисованного экрана.
            pygame.display.flip()

    def _update_bullets(self):
        self.bullets.update()

        # Удаление снарядов, вышедших за край экран.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Обработка коллизий снарядов с пришельцами."""
        # Удаление снарядов и пришельцев, участвующих в коллизиях.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                alien_explosion_sound.play()
            self.sb.prep_score()
            self._check_high_score()

            # Генерация бонусов
            if random.random() < 0.1:  # Шанс появления бонуса
                bonus_type = random.choice(['life', 'shield', 'power'])
                bonus = Bonus(self, bonus_type)
                self.bonuses.add(bonus)

        if not self.aliens:
            # Уничтожение существующих снарядов и создание нового флота.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Увеличение уровня
            self.stats.level += 1
            self.sb.prep_level()

    def _check_bonus_collisions(self):
        """Проверка столкновений бонусов с кораблем."""
        # Проверка столкновений бонусов с кораблем
        collisions = pygame.sprite.spritecollide(self.ship, self.bonuses, True)

        if collisions:
            for bonus in collisions:
                if bonus.bonus_type == 'life':
                    if self.stats.ships_left < self.settings.ship_limit:
                        self.stats.ships_left += 1  # Увеличиваем количество жизней
                        self.sb.prep_ships()  # Обновляем отображение сердечек
                elif bonus.bonus_type == 'shield':
                    self.ship.shield_active = True  # Включаем щит для корабля
                elif bonus.bonus_type == 'power':
                    self._upgrade_bullet()  # Улучшаем снаряд

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев во флоте."""
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка коллизий "пришелец - корабль".
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Проверить, добрались ли пришельцы до нижнего края экрана.
        self._check_aliens_bottom()

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        # Рисуем фон
        self.screen.blit(self.background_image, self.settings.background_rect)
        
        # Рисуем корабль
        self.ship.blitme()

        # Обновление бонусов
        self.bonuses.update()
        for bonus in self.bonuses.sprites():
            bonus.draw(self.screen)

        # Рисуем пули
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Рисуем инопланетян
        self.aliens.draw(self.screen)

        # Отображаем счет
        self.sb.show_score()

        # Если игра не активна, рисуем кнопку "Играть"
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Обновляем экран
        pygame.display.flip()

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.USEREVENT:
                self.ship.deactivate_shield()  # Окончание действия щита
            elif event.type == pygame.USEREVENT + 1:
                self.ship.deactivate_power()  # Окончание действия усиленных снарядов

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Сброс игровой статистики.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Очистка списков пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()

            # Указатель мыши скрывается.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_s:
            self.save_game_progress()
        elif event.key == pygame.K_l:
            self.load_game_progress()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            laser_sound.play()  

    def save_game_progress(self):
            """Сохраняет текущие данные игры в файл."""
            game_data = {
                "level": self.stats.level,
                "score": self.stats.score,
                "lives": self.stats.ships_left
            }
            save_game(game_data)
            print("Игра сохранена.")

    def load_game_progress(self):
        """Загружает данные игры из файла."""
        game_data = load_game()
        if game_data:
            self.stats.level = game_data["level"]
            self.stats.score = game_data["score"]
            self.stats.ships_left = game_data["lives"]
            self.sb.prep_score()  # Обновляем отображение очков и уровня
            self.sb.prep_level()
            self.sb.prep_ships()
            print(f"Игра загружена. Уровень: {self.stats.level}, Очки: {self.stats.score}, Жизни: {self.stats.ships_left}")

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
