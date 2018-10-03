# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 09:54:15 2018

@author: Administrator
"""

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示单个外星人的类"""
    def __init__(self, ai_settings, screen):
        """initialize the alien and set its position"""
        super(Alien, self).__init__()#似乎是一种继承
        self.screen = screen
        self.ai_settings = ai_settings
        
        #加载外星人图像，并设置其rect属性
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        
        #每个外星人最初在左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #存储外星人的准确位置
        self.x = float(self.rect.x)
        
    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)
    
    def update(self):
        """向右移动外星人"""
        self.x += (self.ai_settings.alien_speed_factor * 
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x
    
    def check_edges(self):
        """if the alien is on the edge, then return True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True