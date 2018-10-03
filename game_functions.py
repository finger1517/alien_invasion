# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 22:23:25 2018

@author: Administrator
"""

import sys

import pygame

from bullet import Bullet
from alien import Alien
from time import sleep



def check_keydown_events(event,ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

        
def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
        
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # monitor the typeboard and mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """玩家按play时开始新游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        
        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
        #清空外星人和子弹列表
        aliens.empty()
        bullets.empty()
        
        #创建一群新的外星人使飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        
        
            
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
        #recolor the screen in every loop
        screen.fill(ai_settings.bg_color)
        
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        
        ship.blitme()
        aliens.draw(screen)
        #显示得分
        sb.show_score()
        
        if not stats.game_active:
            play_button.draw_button()
        
        # let the thing in the screen seeable
        pygame.display.flip()
        
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置并删除已经消失的子弹"""
    #更新子弹位置
    bullets.update()
    #删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)
        
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    #检查子弹是否击中外星人，如果是这样，就删除子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
        
    if len(aliens) == 0:
        # 如果整群外星人被消灭，就提高一个等级
        bullets.empty()
        ai_settings.increase_speed()
        
        #提高等级
        stats.level += 1
        sb.prep_level()
        
        
        
        create_fleet(ai_settings, screen, ship, aliens)    

def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有达到限制就发射一颗子弹"""
    #创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        
def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    #创建一个外星人，并计算一行可容纳多少外星人
    #外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


    
def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int((available_space_x)/(2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    
def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
    
    
    
    
def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
        
def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        
        #更新记分牌
        sb.prep_ships()
        
        # empty the list
        aliens.empty()
        bullets.empty()
        
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break
        
def check_high_score(stats, sb):
    """检查是否诞生了最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        
    
        
