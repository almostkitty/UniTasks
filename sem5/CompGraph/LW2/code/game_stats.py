

class GameStats():
    """Отслеживание статистики для игры alien Invasion"""

    def __init__(self, ai_game):
        """Инициализирует статистику."""
        self.settings = ai_game.settings
        self.reset_stats()

        # Игра запускатеся в активном состоянии.
        self.game_active = True

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.settings.ship_limit
