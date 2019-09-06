import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen, image_url):
        """Инициализирует корабль и создает его начаьную позицию"""
        super(Ship, self).__init__()
        self.screen = screen
        self.image_url = image_url
        # Загрузка изображения корабля и получение прямоугольника
        self.image = pygame.image.load(image_url)
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.rect = self.image.get_rect()
        # Каждый новый корабль поялвяется у нижнего края экрана
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.moving_right = False  # Флаг перемещения вправо
        self.moving_left = False  # Флаг перемещени влево

    def center_ship(self):
        """Размещает корабль в центре нижней стороны"""
        self.center = self.screen_rect.centerx

    def update(self):
        """Обновляет позицию корабля с учетом флага"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)


