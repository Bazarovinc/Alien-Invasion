import pygame
from pygame.sprite import Sprite


class Life_Ship(Sprite):

    def __init__(self, screen, image_url):
        super(Life_Ship, self).__init__()
        self.screen = screen
        # Загрузка изображения корабля и чение прямоугольника
        self.image_url = image_url
        self.image = pygame.image.load(image_url)
        self.screen_rect = screen.get_rect()
        #self.scale = pygame.transform.scale(self.image, (self.image.get_width() // 15, self.image.get_height() // 100))
        self.rect = self.image.get_rect()