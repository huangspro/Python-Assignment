import core
import sys
import time
import random
import pygame
import sqlite3

from modules.interfaces.Interface import GameStartInterface, GameEndInterface
from modules.spirits.Dinosaur import Dinosaur
from modules.spirits.Obstacle import Cactus, Ptera
from modules.spirits.Scene import Ground, Cloud, Scoreboard


def main(highest_score):
    pygame.init()
    screen = pygame.display.set_mode(core.SCREENSIZE)
    pygame.display.set_caption('Dino Rush')

    # sounds
    sounds = {
        key: pygame.mixer.Sound(value)
        for key, value in core.AUDIO_PATHS.items()
    }

    GameStartInterface(screen, sounds, core)

    score = 0
    dino = Dinosaur(core.IMAGE_PATHS['dino'])

    ground = Ground(
        core.IMAGE_PATHS['ground'],
        position=(0, core.SCREENSIZE[1] * 0.93)
    )

    # sprite groups
    cloud_group = pygame.sprite.Group()
    cactus_group = pygame.sprite.Group()
    ptera_group = pygame.sprite.Group()

    clock = pygame.time.Clock()
    add_obstacle_timer = 0
    score_timer = 0

    score_board = Scoreboard(
        core.FONT_PATHS['joystix'],
        position=(900, 50)
    )

    high_score_board = Scoreboard(
        core.FONT_PATHS['joystix'],
        position=(650, 50),
        is_highest=True
    )

    high_score_board.update_score(highest_score)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    dino.jump(sounds)
                elif event.key == pygame.K_DOWN:
                    dino.duck()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dino.unduck()

        screen.fill(core.BACKGROUND_COLOR)

        if len(cloud_group) < 5 and random.randint(0, 250) == 10:
            cloud_group.add(
                Cloud(
                    core.IMAGE_PATHS['cloud'],
                    position=(core.SCREENSIZE[0], random.randint(50, 500))
                )
            )


        add_obstacle_timer += 1

        if add_obstacle_timer > 60:
            add_obstacle_timer = 0

            if random.random() < 0.8:
                cactus_group.add(
                    Cactus(
                        core.IMAGE_PATHS['cacti'],
                        position=(core.SCREENSIZE[0], int(core.SCREENSIZE[1] * 0.93))
                    )
                )
            else:
                ptera_group.add(
                    Ptera(
                        core.IMAGE_PATHS['ptera'],
                        position=(core.SCREENSIZE[0], random.choice([core.SCREENSIZE[1]*0.7, core.SCREENSIZE[1]*0.6, core.SCREENSIZE[1]*0.5]))
                    )
                )

        dino.update()
        ground.update()

        cloud_group.update()
        cactus_group.update()
        ptera_group.update()

        score_timer += 1

        if score_timer % 5 == 0:
            score += 1

            if score % 100 == 0:
                sounds['point'].play()

            # difficulty scaling
            if score % 1000 == 0:
                ground.speed -= 1
                for obj in cactus_group:
                    obj.speed -= 1
                for obj in ptera_group:
                    obj.speed -= 1

        # update scoreboards (NO recreation)
        score_board.update_score(score)
        highest_score = max(highest_score, score)
        high_score_board.update_score(highest_score)

        for cactus in cactus_group:
            if pygame.sprite.collide_mask(dino, cactus):
                dino.is_dead = True
                sounds['die'].play()

        for ptera in ptera_group:
            if pygame.sprite.collide_mask(dino, ptera):
                dino.is_dead = True
                sounds['die'].play()

        for cloud in cloud_group:
            cloud.draw(screen)

        dino.draw(screen)
        ground.draw(screen)

        for cactus in cactus_group:
            cactus.draw(screen)

        for ptera in ptera_group:
            ptera.draw(screen)

        high_score_board.draw(screen)
        score_board.draw(screen)

        pygame.display.update()
        clock.tick(core.FPS)

        if dino.is_dead:

            c.execute(
                "INSERT INTO record VALUES (?, ?)",
                (int(time.time()), score)
            )

            highest_score = max(highest_score, score)
            break

    return GameEndInterface(screen, core), highest_score


if __name__ == '__main__':

    conn = sqlite3.connect('history.db')
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS record (
            unix_timestamp INT PRIMARY KEY,
            score SMALLINT NOT NULL
        );
    """)

    c.execute("SELECT MAX(score) FROM record;")
    row = c.fetchone()

    highest_score = row[0] if row and row[0] is not None else 0

    while True:
        flag, highest_score = main(highest_score)
        if not flag:
            break

    conn.commit()
    conn.close()
