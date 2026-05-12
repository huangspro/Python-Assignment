import pygame


class Dinosaur(pygame.sprite.Sprite):
    """Dinosaur player class"""

    def __init__(
        self,
        imagepaths,
        position=(40, 1100),
        size=[(132, 141), (177, 141)],
        **kwargs
    ):

        pygame.sprite.Sprite.__init__(self)

        # Load animation frames
        self.images = []

        # Normal running frames
        image = pygame.image.load(imagepaths[0])
        for i in range(5):
            self.images.append(
                pygame.transform.scale(
                    image.subsurface((i * 44, 0), (44, 47)),
                    size[0]
                )
            )

        # Ducking frames
        image = pygame.image.load(imagepaths[1])
        for i in range(2):
            self.images.append(
                pygame.transform.scale(
                    image.subsurface((i * 59, 0), (59, 47)),
                    size[1]
                )
            )

        # Initial image
        self.image_idx = 0
        self.image = self.images[self.image_idx]

        # Position
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.bottom = position

        # Collision mask
        self.mask = pygame.mask.from_surface(self.image)

        # Physics
        self.init_position = position
        self.refresh_rate = 5
        self.refresh_counter = 0

        self.speed = 20
        self.gravity = 0.7

        # State flags
        self.is_jumping = False
        self.is_ducking = False
        self.is_dead = False

        # Movement [x, y]
        self.movement = [0, 0]

    def jump(self, sounds):
        """Make dinosaur jump"""

        # Cannot jump twice
        if self.is_dead:
            return

        # Play sound
        sounds['jump'].play()

        # Start jumping
        self.is_jumping = True
        self.movement[1] = -self.speed

    def duck(self):
        """Start ducking"""

        # Duck only on ground
        if not self.is_jumping and not self.is_dead:
            self.is_ducking = True

    def unduck(self):
        """Stop ducking"""

        self.is_ducking = False

    def die(self, sounds):
        """Set death state"""

        # Play death sound
        sounds['die'].play()

        # Set dead state
        self.is_dead = True

    def draw(self, screen):
        """Draw dinosaur"""

        screen.blit(self.image, self.rect)

    def loadImage(self):
        """Update image and mask"""

        # Save current position
        left = self.rect.left
        bottom = self.rect.bottom

        # Update image
        self.image = self.images[self.image_idx]

        # Update rect
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.bottom = bottom

        # Update mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """Update dinosaur state"""

        # Dead state
        if self.is_dead:

            self.image_idx = 4

        # Jumping state
        elif self.is_jumping:

            # Apply gravity
            self.movement[1] += self.gravity
            self.rect.top += self.movement[1]

            # Landing
            if self.rect.bottom >= self.init_position[1]:
                self.rect.bottom = self.init_position[1]
                self.is_jumping = False
                self.movement[1] = 0

            self.image_idx = 0

        # Ducking state
        elif self.is_ducking:

            # Duck animation
            if self.refresh_counter % self.refresh_rate == 0:

                if self.image_idx == 5:
                    self.image_idx = 6
                else:
                    self.image_idx = 5

        # Running state
        else:

            # Running animation
            if self.refresh_counter % self.refresh_rate == 0:
                self.image_idx += 1

                if self.image_idx >= 4:
                    self.image_idx = 0

        # Update frame counter
        self.refresh_counter += 1

        # Load current frame
        self.loadImage()
