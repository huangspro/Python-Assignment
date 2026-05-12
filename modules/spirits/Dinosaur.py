#### 代码框架

import pygame

class Dinosaur(pygame.sprite.Sprite):
    """恐龙角色类"""
    
    def __init__(self, imagepaths, position=(40, 535), size=[(132, 141), (177, 141)], **kwargs):
        """
        初始化恐龙角色       
        Args:
            imagepaths (list): 恐龙图片路径列表 [正常状态, 下蹲状态]
            position (tuple): 恐龙在屏幕上的初始位置
            size (list): 恐龙图片的缩放尺寸 [正常尺寸, 下蹲尺寸]
        """

        pygame.sprite.Sprite.__init__(self)
        
        # 加载恐龙的所有动画帧图片
        self.images = []
        # 提示：正常状态有5帧动画，下蹲状态有2帧动画
        image = pygame.image.load(imagepaths[0])
        for i in range(5):
            self.images.append(pygame.transform.scale(image.subsurface((i * 44, 0), (44, 47)), size[0]))
        image = pygame.image.load(imagepaths[1])
        for i in range(2):
            self.images.append(pygame.transform.scale(image.subsurface((i * 59, 0), (59, 47)), size[1]))

        # TODO: 设置恐龙的初始图片和位置
        self.image_idx = 0
        self.image = self.images[self.image_idx]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = position
        self.mask = pygame.mask.from_surface(self.image)
        
        # 恐龙的物理属性
        self.init_position = position
        self.refresh_rate = 5  # 动画刷新频率
        self.refresh_counter = 0
        self.speed = 20  # 跳跃初始速度
        self.gravity = 0.7  # 重力加速度
        self.is_jumping = False
        self.is_ducking = False
        self.is_dead = False
        self.movement = [0, 0]  # [水平移动, 垂直移动]

    def jump(self, sounds):
        """
        恐龙跳跃方法      
        Args:
            sounds (dict): 音效字典
        """
        # TODO: 实现跳跃逻辑# 提示：检查是否已经在跳跃或死亡状态，播放跳跃音效，设置垂直移动速度
        pass
    
    def duck(self):
        """恐龙下蹲方法"""
        # TODO: 实现下蹲逻辑# 提示：检查是否在跳跃或死亡状态，设置下蹲标志 
        pass
    
    def unduck(self):
        """恐龙停止下蹲方法"""
        # TODO: 取消下蹲状态
        pass
    
    def die(self, sounds):
        """
        恐龙死亡方法        
        Args:
            sounds (dict): 音效字典
        """
        # TODO: 实现死亡逻辑
        # 提示：播放死亡音效，设置死亡标志
        pass
    
    def draw(self, screen):
        """
        在屏幕上绘制恐龙
        
        Args:
            screen: Pygame屏幕对象
        """
        # TODO: 将恐龙图片绘制到屏幕上
        pass
    
    def loadImage(self):
        """加载当前帧的图片并更新碰撞遮罩"""
        # TODO: 根据当前图片索引加载图片，更新rect和mask
        pass
    
    def update(self):
        """更新恐龙状态（每帧调用）"""
        # TODO: 实现恐龙状态更新逻辑
        # 包括：死亡状态、跳跃物理、下蹲动画、正常跑步动画
        pass


