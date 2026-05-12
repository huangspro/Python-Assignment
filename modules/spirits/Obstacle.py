#### 代码框架

import random
import pygame

class Cactus(pygame.sprite.Sprite):
    """仙人掌障碍物类"""
    
    def __init__(self, imagepaths, position=(1200, 545), sizes=[(204, 204), (153, 114)], **kwargs):

        

        """
        初始化仙人掌障碍物
        Args:
            imagepaths (list): 仙人掌图片路径列表
            position (tuple): 初始位置
            sizes (list): 不同类型仙人掌的尺寸
        """
        pygame.sprite.Sprite.__init__(self)
        
        # TODO: 加载不同类型的仙人掌图片
        self.images = []
        # 提示：大仙人掌有3种变体，小仙人掌有2种变体
        
        # TODO: 随机选择一种仙人掌类型
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = position
        self.mask = pygame.mask.from_surface(self.image)
        
        self.speed = -10  # 向左移动速度
    
    def draw(self, screen):
        """绘制仙人掌到屏幕"""
        # TODO: 实现绘制逻辑
        pass
    
    def update(self):
        """更新仙人掌位置"""
        # TODO: 实现移动逻辑，移出屏幕后自动销毁
        pass

class Ptera(pygame.sprite.Sprite):
    """翼龙障碍物类"""
    
    def __init__(self, imagepath, position, size=(138, 126), **kwargs):
        """
        初始化翼龙障碍物
        

        Args:
            imagepath (str): 翼龙图片路径
            position (tuple): 初始位置
            size (tuple): 翼龙尺寸
        """
        pygame.sprite.Sprite.__init__(self)
        
        # TODO: 加载翼龙的飞行动画帧
        self.images = []
        # 提示：翼龙有2帧飞行动画
        
        self.image_idx = 0
        self.image = self.images[self.image_idx]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.centery = position
        self.mask = pygame.mask.from_surface(self.image)
        
        self.speed = -10  # 向左移动速度
        self.refresh_rate = 10  # 动画刷新频率

        self.refresh_counter = 0
    
    def draw(self, screen):
        """绘制翼龙到屏幕"""
        # TODO: 实现绘制逻辑
        pass
    
    def update(self):
        """更新翼龙位置和动画"""
        # TODO: 实现飞行动画和移动逻辑
        pass
    
    def loadImage(self):
        """加载当前帧的翼龙图片"""
        # TODO: 更新翼龙的当前动画帧
        pass


