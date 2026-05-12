import sys
import pygame
from modules.spirits.Dinosaur import Dinosaur


def GameStartInterface(screen, sounds, cfg):
    """
    Game start interface

    Args:
        screen: pygame screen
        sounds (dict): sound effects
        cfg: config module

    Returns:
        bool: start game or not
    """

    # Create title text
    title_font = pygame.font.Font(cfg.FONT_PATHS['joystix'], 40)
    title_text = title_font.render(
        "D I N O  R U S H",
        True,
        cfg.BLACK
    )
    title_rect = title_text.get_rect()
    title_rect.centerx = cfg.SCREENSIZE[0] // 2
    title_rect.top = 120

    # Create designer text
    info_font = pygame.font.Font(cfg.FONT_PATHS['joystix'], 20)
    info_text = info_font.render(
        "DESIGNED BY Haoyu Huang/SUAT25000228",
        True,
        cfg.BLACK
    )
    info_rect = info_text.get_rect()
    info_rect.centerx = cfg.SCREENSIZE[0] // 2
    info_rect.top = 180

    # Create dinosaur
    dino = Dinosaur(cfg.IMAGE_PATHS['dino'])

    # Load ground image
    ground_image = pygame.image.load(
        cfg.IMAGE_PATHS['ground']
    ).convert_alpha()

    ground_rect = ground_image.get_rect()
    ground_rect.left = 0
    ground_rect.bottom = cfg.SCREENSIZE[1]

    clock = pygame.time.Clock()

    # Main loop
    while True:

        # Event handling
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Start game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or \
                   event.key == pygame.K_UP:

                    sounds['jump'].play()
                    return True

        # Update dinosaur animation
        dino.update()

        # Draw background
        screen.fill(cfg.BACKGROUND_COLOR)

        # Draw ground
        screen.blit(ground_image, ground_rect)

        # Draw texts
        screen.blit(title_text, title_rect)
        screen.blit(info_text, info_rect)

        # Draw dinosaur
        dino.draw(screen)

        pygame.display.update()
        clock.tick(cfg.FPS)


import sys
import pygame


def GameEndInterface(screen, cfg):
    """
    Game over interface

    Args:
        screen: pygame screen
        cfg: config module

    Returns:
        bool: restart game or not
    """

    # Load replay button
    replay_image = pygame.image.load(
        cfg.IMAGE_PATHS['replay']
    ).convert_alpha()

    replay_rect = replay_image.get_rect()
    replay_rect.centerx = cfg.SCREENSIZE[0] // 2
    replay_rect.centery = cfg.SCREENSIZE[1] // 2 + 50

    # Create GAME OVER text
    title_font = pygame.font.Font(cfg.FONT_PATHS['joystix'], 35)

    gameover_text = title_font.render(
        "GAME OVER",
        True,
        cfg.BLACK
    )

    gameover_rect = gameover_text.get_rect()
    gameover_rect.centerx = cfg.SCREENSIZE[0] // 2
    gameover_rect.centery = cfg.SCREENSIZE[1] // 2 - 40

    # Create hint text
    hint_font = pygame.font.Font(cfg.FONT_PATHS['joystix'], 18)

    hint_text = hint_font.render(
        "PRESS [SPACE]/[ UP ] TO CONTINUE",
        True,
        cfg.BLACK
    )

    hint_rect = hint_text.get_rect()
    hint_rect.centerx = cfg.SCREENSIZE[0] // 2
    hint_rect.centery = cfg.SCREENSIZE[1] // 2

    clock = pygame.time.Clock()

    # Main loop
    while True:

        # Event handling
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Keyboard restart
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or \
                   event.key == pygame.K_UP:
                    return True

            # Mouse click restart
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_rect.collidepoint(event.pos):
                    return True

        # Draw background
        screen.fill(cfg.BACKGROUND_COLOR)

        # Draw texts
        screen.blit(gameover_text, gameover_rect)
        screen.blit(hint_text, hint_rect)

        # Draw replay button
        screen.blit(replay_image, replay_rect)

        pygame.display.update()
        clock.tick(cfg.FPS)
