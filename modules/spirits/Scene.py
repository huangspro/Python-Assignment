import pygame
import random
import pickle
import os

class Ground(pygame.sprite.Sprite):
    """Infinite scrolling ground"""

    def __init__(self, imagepath, position, speed=-10):
        super().__init__()

        self.image = pygame.image.load(imagepath).convert_alpha()

        self.rect_1 = self.image.get_rect()
        self.rect_2 = self.image.get_rect()

        self.rect_1.left, self.rect_1.top = position
        self.rect_2.left = self.rect_1.right
        self.rect_2.top = position[1]

        self.speed = speed

    def update(self):
        self.rect_1.left += self.speed
        self.rect_2.left += self.speed

        # loop scrolling
        if self.rect_1.right <= 0:
            self.rect_1.left = self.rect_2.right

        if self.rect_2.right <= 0:
            self.rect_2.left = self.rect_1.right

    def draw(self, screen):
        screen.blit(self.image, self.rect_1)
        screen.blit(self.image, self.rect_2)


class Cloud(pygame.sprite.Sprite):
    """Floating cloud with configurable size and speed"""

    def __init__(
        self,
        imagepath,
        position,
        scale=(92, 54),
        speed_range=(-2, -1),
    ):
        super().__init__()

        image = pygame.image.load(imagepath).convert_alpha()

        # scalable cloud size
        self.image = pygame.transform.smoothscale(image, scale)

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position

        # random speed for natural movement
        self.speed = random.randint(speed_range[0], speed_range[1])

    def update(self):
        self.rect.left += self.speed

        # remove when off screen
        if self.rect.right < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)





class Scoreboard(pygame.sprite.Sprite):
    """Score display with optional persistent highest score"""

    def __init__(self, fontpath, position, is_highest=False, save_file='score.pkl'):
        super().__init__()

        self.font = pygame.font.Font(fontpath, 32)
        self.position = position
        self.is_highest = is_highest
        self.save_file = save_file

        self.score = 0
        self.image = None
        self.rect = None

        if self.is_highest:
            self.score = self.load_score()

        self.update_score(self.score)

    def load_score(self):
        if not os.path.exists(self.save_file):
            return 0
        try:
            with open(self.save_file, 'rb') as f:
                return pickle.load(f)
        except:
            return 0

    def save_score(self, score):
        try:
            with open(self.save_file, 'wb') as f:
                pickle.dump(score, f)
        except:
            pass

    def update_score(self, score):
        self.score = score

        text = str(score).zfill(5)
        if self.is_highest:
            text = "HI " + text

        self.image = self.font.render(text, True, (83, 83, 83))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

    def draw(self, screen):
        screen.blit(self.image, self.rect)
