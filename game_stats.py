class GameStats():
    """Отслеживание статистики для игры Alien Invasion"""

    def __init__(self, ai_settings):
        """Инициализирует статистику"""
        self.ai_settings = ai_settings
        self.reset_stats()
        # Игра запускается в неактивном состоянии
        self.game_active = False
        # Рекорд не должен сбрасываться
        self.high_score = self.get_high_score()

    def reset_stats(self):
        """Инициализирует статистику, изменяющусся в ходе игры."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def get_high_score(self):
        f_name = 'high_score.txt'
        try:
            with open(f_name, 'r') as f_obj:
                high_score = f_obj.read()
                high_score = int(high_score)
        except FileNotFoundError:
            high_score = 0
            with open(f_name, 'w') as f_obj:
                f_obj.write(str(high_score))
        return high_score

