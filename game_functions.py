import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, life_ship_url, alien_url):
    """Обрабатывает столкновение корабля с пришельцем."""
    # Уменьшение ships_left.
    if stats.ships_left > 0:
        stats.ships_left -= 1
        # Обновление игровой информации
        sb.prep_ships(life_ship_url)
        # Очистка списков пришельцев и пуль.
        aliens.empty()
        bullets.empty()
        # Создание нового флота и размещение корабля в центре.
        create_fleet(ai_settings, screen, ship, aliens, alien_url)
        ship.center_ship()
        # Пауза.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
        save_high_score(stats)


def save_high_score(stats):
    f_name = 'high_score.txt'
    if int(stats.score) > int(stats.high_score):
        stats.high_score = stats.score
    with open(f_name, 'w') as f_obj:
        f_obj.write(str(stats.high_score))


def check_keydown_events(event, ai_settings, screen, stats, ship, bullets):
    """Реагирует на нажатие клавишь"""
    if event.key == pygame.K_RIGHT:
        # Переместить корабль
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Переместить корабль
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    """elif event.key == pygame.K_ESCAPE:
        stats.game_active = False
        pygame.mouse.set_visible(True)"""


def fire_bullet(ai_settings, screen, ship, bullets):
    """Выпускает пулю, если максимум еще не достигнут"""
    # Создание новой пули и включение ее в группу bullets
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """Реагирует на отпускание клавишь"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, life_ship_url, alien_url):
    """Обрабатывает нажатие клавишь и события мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y,
                              life_ship_url, alien_url)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y,
                      life_ship_url, alien_url):
    """Запускает новую игру при нажатии на кнопку Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Сброси игровых настроек
        ai_settings.initialize_dynamic_settings()
        # Указатель мыши скрывается
        pygame.mouse.set_visible(False)
        # Сброси игровой статисктики
        stats.reset_stats()
        stats.game_active = True
        # Сброс изображений счетов и уровня
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships(life_ship_url)
        # Очитстка списков пришельцев и пуль
        aliens.empty()
        bullets.empty()
        # Создание нового флота и рамещение корабля в центре.
        create_fleet(ai_settings, screen, ship, aliens, alien_url)
        ship.center_ship()


def check_high_score(stats, sb):
    """Проверяет, появился ли новый рекорд"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Обновляет позиции пуль и уничтожает старые"""
    # Обновление позиций пуль
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # Проверка попаданий в пришельцев
    # При обнаружении пападания удалитьь пулю и пришельца.
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряду"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Определяет количество рядов, помещающихся на экране"""
    available_space_y = (ai_settings.screen_height - (6 * alien_height)-ship_height)
    number_rows = int(available_space_y/(2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number, alien_url):
    """Создает пришельца и размещает его в ряду"""
    alien = Alien(ai_settings, screen, alien_url)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens, alien_url):
    """Создает флот пришельцев"""
    # Создание пришельца и вычисление количества пришельцев в ряду
    alien = Alien(ai_settings, screen, alien_url)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # Создание первого ряда пришельцев
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number, alien_url)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Обработка коллизий пуль с пришельцами"""
    # Удаление пули и пришельца участвующих в коллизиии
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)
    if len(aliens) == 0:
        # Уничтожение существующих пуль и создание нового флота, с увеличением скрости
        bullets.empty()
        ai_settings.increase_speed()
        # Увеличение уровня
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достиения пришельцем экрана"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Проверяет, добрались ли пришельцы до нижнего края экрана"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Происходит то же, что при столкновении с кораблем
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, life_ship_url, alien_url):
    """Проверяет, достиг ли флот края экрана,после чего обновляет позиции всех пришельцев во флоте."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Проверка коллизий "пришелец корабль"
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, life_ship_url, alien_url)
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Обновляет изображения на экране и отображает новый экран."""
    screen.blit(ai_settings.bg_color, [0, 0])
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # Кнопка Play отображается в том случае, если игра неактивна.
    if not stats.game_active:
        play_button.draw_button()
    sb.show_score()

    # Отображение последнего прорисованного экрана.
    pygame.display.flip()
