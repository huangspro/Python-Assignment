#### 代码框架
import pygame

class Ground(pygame.sprite.Sprite):
    """地面类"""    
    def __init__(self, imagepath, position, **kwargs):
        """
        初始化地面        
        Args:
            imagepath (str): 地面图片路径
            position (tuple): 地面位置
        """
        pygame.sprite.Sprite.__init__(self)       
        # TODO: 创建两个地面图片实现无限滚动
        # 提示：使用两个rect来实现无缝连接
        self.speed = -10  # 地面移动速度

    def update(self):
        """更新地面位置实现滚动效果"""
        # TODO: 实现地面无限滚动逻辑
        pass
    
    def draw(self, screen):
        """绘制地面到屏幕"""
        # TODO: 绘制两个地面图片
        pass

class Cloud(pygame.sprite.Sprite):
    """云朵类"""
    
    def __init__(self, imagepath, position, **kwargs):
        """
        初始化云朵
        
        Args:
            imagepath (str): 云朵图片路径
            position (tuple): 云朵位置
        """

        pygame.sprite.Sprite.__init__(self)
        
        # TODO: 加载和缩放云朵图片
        self.speed = -1  # 云朵移动速度（比地面慢）
    
    def draw(self, screen):
        """绘制云朵到屏幕"""
        # TODO: 实现绘制逻辑
        pass
    
    def update(self):
        """更新云朵位置"""
        # TODO: 实现移动逻辑，移出屏幕后自动销毁
        pass

class Scoreboard(pygame.sprite.Sprite):
    """计分板类"""
    
    def __init__(self, score, fontpath, position, is_highest=False):
        """
        初始化计分板
        
        Args:
            score (int): 要显示的分数
            fontpath (str): 字体文件路径
            position (tuple): 计分板位置
            is_highest (bool): 是否为最高分显示
        """
        pygame.sprite.Sprite.__init__(self)
        
        # TODO: 创建分数文本渲染
        # 提示：最高分前面要加"HI"前缀，分数要补零到5位
        pass
    
    def draw(self, screen):
        """绘制计分板到屏幕"""
        # TODO: 实现绘制逻辑
        pass


