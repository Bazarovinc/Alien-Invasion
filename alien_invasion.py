from os import path
from typing import Union

import pygame
import os
import sys

from pygame.sprite import Group

from settings import Settings

from game_stats import GameStats

from ship import Ship

from button import Button

from score_board import Scoreboard

import game_functions as gf


def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

spaceraft_url = resource_path('spacecraft_3.png')
alien_url = resource_path('alien_1.2.png')
life_ship_url = resource_path('Life_ship.png')
bg_url = resource_path('new_space.jpg')

def run_game():
    # Инициализирует игру и создает объект экрана
    pygame.init()
    ai_settings = Settings(bg_url)
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Alien Invasion")
    # Создание кнопки Play
    play_button = Button(ai_settings, screen, "Play")
    # Создание корабля
    ship = Ship(ai_settings, screen, spaceraft_url)
    # создание экземпляра для хранение игровой статистик
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats, life_ship_url)
    # Создание группы для хранения пуль
    bullets = Group()
    aliens = Group()
    # Создание флота пришельцев
    gf.create_fleet(ai_settings, screen, ship, aliens, alien_url)
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, life_ship_url, alien_url)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, life_ship_url, alien_url)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

run_game()