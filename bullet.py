# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 23:08:30 2018

@author: Administrator
"""

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """一个对飞船发射的子弹进行管理的类"""
    
    def __init__(self, ai_settings, screen, ship):
        """creat a bullet in where the ship is"""
        super(Bullet, self).__init__()
        self.screen = screen
        
        #(0,0)set the bullet and set the right position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        #save the position in float forms
        self.y = float(self.rect.y)
        
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
        
    def update(self):
        """向上移动子弹"""
        #update the position
        self.y -= self.speed_factor
        #update the rect position
        self.rect.y = self.y
        
    def draw_bullet(self):
        """draw the bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)