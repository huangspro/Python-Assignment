import core
import sys
import time
import random
import pygame
import sqlite3
import pickle
import random
import os
import numpy
import torch

from modules.interfaces.Interface import GameStartInterface, GameEndInterface
from modules.spirits.Dinosaur import Dinosaur
from modules.spirits.Obstacle import Cactus, Ptera
from modules.spirits.Scene import Ground, Cloud, Scoreboard

# RL implemention==========================================================================================================
greedy = 0.2
learning_ratio = 0.0001
discounted = 0.99
device = torch.device('cpu')

class Q(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.linear1 = torch.nn.Linear(20+1, 14)
        self.linear2 = torch.nn.Linear(14, 28)
        self.linear3 = torch.nn.Linear(28, 14)
        self.linear4 = torch.nn.Linear(14, 1)
    def forward(self, state, action):  
        action = torch.tensor([action], dtype=torch.float32).to(device)
        print(state.shape)
        x = torch.nn.functional.relu(self.linear1(torch.cat([state, action])))
        x = torch.nn.functional.relu(self.linear2(x))
        x = torch.nn.functional.relu(self.linear3(x))
        x = self.linear4(x)
        return x

def pack(dino, cactus_group, ptera_group):

    def get_corners(sprite):
        r = sprite.rect
        x, y = r.left, r.top
        w, h = r.width, r.height
        return [
            x, y,
            x + w, y + h,
        ]

    features = []
    features.extend(get_corners(dino))

    cactus_list = sorted(cactus_group, key=lambda s: s.rect.x)
    if len(cactus_list)==2:
        for c in sorted(cactus_group, key=lambda s: s.rect.x)[:2]:
            features.extend(get_corners(c))
    else:
        features.extend([0.0] * 4 if len(cactus_list)==1 else [0.0]*8)   # padding
        
    ptera_list = sorted(ptera_group, key=lambda s: s.rect.x)
    if len(ptera_list)==2:
        for c in sorted(ptera_group, key=lambda s: s.rect.x)[:2]:
            features.extend(get_corners(c))
    else:
        features.extend([0.0] * 4 if len(ptera_list)==1 else [0.0]*8)   # padding
        
    return torch.tensor(features, dtype=torch.float32)

def take_action(s):
    a = random.random()
    if a>greedy:
        actions = [0,1]
        output = []
        for action in actions:
            output.append(Q_model(s, action).detach().squeeze())
        return actions[output.index(max(output))]   
    else:
        return random.randint(0, 3)

def find_max(s):
    actions = [0,1]
    output = []
    for action in actions:
        output.append(Q_model(s, action).detach().squeeze())
    return max(output)
    
Q_model = Q().to(device)
#Q_model = torch.load("model.pth", weights_only=False).to(device)
optimizer = torch.optim.Adam(Q_model.parameters(), lr=learning_ratio)
#==========================================================================================================
def main(highest_score):
    pygame.init()
    screen = pygame.display.set_mode(core.SCREENSIZE)
    pygame.display.set_caption('Dino Rush')

    # Load sounds
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

    # Sprite groups for obstacles and clouds
    cloud_group = pygame.sprite.Group()
    cactus_group = pygame.sprite.Group()
    ptera_group = pygame.sprite.Group()

    clock = pygame.time.Clock()
    score_timer = 0

    # Initialize scoreboards
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

    epoch = 0
    while True:
        #RL logic=================================================================================================
        epoch+=1
        if(epoch%20==0):
            torch.save(Q_model, "model.pth")
        
        action = take_action(pack(dino,cactus_group, ptera_group))
        old_q = Q_model(pack(dino, cactus_group, ptera_group), action)
        if(action==1) and dino.rect.y > core.SCREENSIZE[1] // 2.5:
            dino.jump(sounds)
            
        with torch.no_grad():
            target = score + discounted * find_max(pack(dino, cactus_group, ptera_group))
        loss = (old_q - target)**2
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        #=================================================================================================
    
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if dino.rect.y > core.SCREENSIZE[1] // 2.5:
                        dino.jump(sounds)
                elif event.key == pygame.K_DOWN:
                    dino.duck()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dino.unduck()

        screen.fill(core.BACKGROUND_COLOR)

        # Cloud generation logic
        if len(cloud_group) < 5 and random.randint(0, 250) == 10:
            cloud_group.add(
                Cloud(
                    core.IMAGE_PATHS['cloud'],
                    position=(core.SCREENSIZE[0], random.randint(50, 500))
                )
            )

        while len(cactus_group) < 2:
            spawn_x = core.SCREENSIZE[0]
            if len(cactus_group) > 0:
                rightmost_cactus = max(cactus_group, key=lambda c: c.rect.right)
                spawn_x = rightmost_cactus.rect.right + 500 
            
            cactus_group.add(
                Cactus(
                    core.IMAGE_PATHS['cacti'],
                    position=(spawn_x, int(core.SCREENSIZE[1] * 0.93))
                )
            )
        while len(cactus_group) > 2:
            cactus_group.sprites()[0].kill()

        # 2. Ensure exactly 2 pteras 
        while len(ptera_group) < 2:
            spawn_x = core.SCREENSIZE[0]
            if len(ptera_group) > 0:
                rightmost_ptera = max(ptera_group, key=lambda p: p.rect.right)
                spawn_x = rightmost_ptera.rect.right + 500
            
            ptera_group.add(
                Ptera(
                    core.IMAGE_PATHS['ptera'],
                    position=(spawn_x, random.choice([core.SCREENSIZE[1]*0.7, core.SCREENSIZE[1]*0.6, core.SCREENSIZE[1]*0.5]))
                )
            )
        while len(ptera_group) > 2:
            ptera_group.sprites()[0].kill()
        # --- End of Fixed Obstacle Control ---

        dino.update()
        ground.update()

        cloud_group.update()
        cactus_group.update()
        ptera_group.update()

        # Score counting logic
        score_timer += 1
        if score_timer % 5 == 0:
            score += 1
            if score % 100 == 0:
                sounds['point'].play()

            # Difficulty scaling
            if score % 1000 == 0:
                ground.speed -= 1
                for obj in cactus_group:
                    obj.speed -= 1
                for obj in ptera_group:
                    obj.speed -= 1

        # Update scoreboards
        score_board.update_score(score)
        highest_score = max(highest_score, score)
        high_score_board.update_score(highest_score)

        # Collision detection
        for cactus in cactus_group:
            if pygame.sprite.collide_mask(dino, cactus):
                dino.is_dead = True
                sounds['die'].play()

        for ptera in ptera_group:
            if pygame.sprite.collide_mask(dino, ptera):
                dino.is_dead = True
                sounds['die'].play()

        # Draw all elements
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

        # Game over logic
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
