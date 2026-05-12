import random
import pygame


class Cactus(pygame.sprite.Sprite):
    """Cactus obstacle"""

    def __init__(self, imagepaths, position=(1200, 1100),
                 sizes=[(204, 204), (153, 114)], **kwargs):
        """
        Initialize cactus
        Args:
            imagepaths (list): cactus image paths
            position (tuple): start position
            sizes (list): cactus sizes
        """
        pygame.sprite.Sprite.__init__(self)

        # Load cactus images
        self.images = []

        # Big cactus: 3 variants
        big_cactus = pygame.image.load(imagepaths[0]).convert_alpha()
        for i in range(3):
            image = pygame.Surface((68, 68), pygame.SRCALPHA)
            image.blit(big_cactus, (0, 0), (i * 68, 0, 68, 68))
            image = pygame.transform.scale(image, sizes[0])
            self.images.append(image)

        # Small cactus: 2 variants
        small_cactus = pygame.image.load(imagepaths[1]).convert_alpha()
        for i in range(2):
            image = pygame.Surface((68, 68), pygame.SRCALPHA)
            image.blit(small_cactus, (0, 0), (i * 68, 0, 68, 68))
            image = pygame.transform.scale(image, sizes[1])
            self.images.append(image)

        # Random cactus
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = position
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = -10

    def draw(self, screen):
        """Draw cactus"""
        screen.blit(self.image, self.rect)

    def update(self):
        """Move cactus"""
        self.rect.left += self.speed

        # Remove when out of screen
        if self.rect.right < 0:
            self.kill()


class Ptera(pygame.sprite.Sprite):
    """Flying obstacle with stable animation"""

    def __init__(self, imagepath, position, size=(138, 126)):
        super().__init__()

        self.images = []

        sheet = pygame.image.load(imagepath).convert_alpha()

        # split frames
        for i in range(2):
            frame = pygame.Surface((46, 41), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (i * 46, 0, 46, 41))
            frame = pygame.transform.scale(frame, size)
            self.images.append(frame)

        self.image_idx = 0
        self.image = self.images[0]

        # anchor position (IMPORTANT)
        self.x = position[0]
        self.y = position[1]

        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.centery = self.y

        self.mask = pygame.mask.from_surface(self.image)

        self.speed = -10

        self.refresh_rate = 10
        self.counter = 0

    def update(self):
        # move
        self.x += self.speed

        # animation
        self.counter += 1
        if self.counter >= self.refresh_rate:
            self.counter = 0
            self.image_idx = (self.image_idx + 1) % len(self.images)
            self.image = self.images[self.image_idx]

            # IMPORTANT: refresh mask when image changes
            self.mask = pygame.mask.from_surface(self.image)

        # update rect from anchor
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.centery = self.y

        # remove off screen
        if self.rect.right < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
