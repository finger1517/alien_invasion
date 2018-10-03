# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 14:02:05 2018

@author: Administrator
"""

class GameStats():
    """跟踪游戏的统计信息"""
    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()
        #一开始处于非活动状态
        self.game_active = False
        
        # 最高分任何情况下都不能重置
        self.high_score = 0
    
    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1