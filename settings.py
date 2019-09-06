import pygame

class Settings():
    """Класс для хранения всех настроек игры Alien Invasion"""

    def __init__(self, image_url):
        """Инициализирует статические настройки игры."""
        # Параметры экрана
        self.screen_width = 1500
        self.screen_height = 800
        self.image_url = image_url
        self.bg_color = pygame.image.load(image_url)  # Импортирование заднего фона
        # Параметры корабля
        self.ship_limit = 3
        # Параметры пуль
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 50, 205, 50
        self.bullets_allowed = 5
        # Параметры пришельцев
        self.fleet_drop_speed = 12
        # Темп ускорения игры
        self.speedup_scale = 1.2
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры"""
        self.ship_speed_factor = 10
        self.bullet_speed_factor = 12
        self.alien_speed_factor = 1
        self.fleet_direction = 1  # 1-движение вправо, -1 движение влево
        # Подсчет очков
        self.alien_points = 50

    def increase_speed(self):
        """Увеличивает настройки скорости и стоимость пришельцев"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

