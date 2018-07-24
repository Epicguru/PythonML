import pygame
from game_entity import GameEntity
import game_state as gs
from sprite import Sprite
import random
from asset_loader import load_image
import game_state as gs


class WindowControlEntity(GameEntity):

    def update(self, dt: float):

        x = gs.camera_pos[0]
        y = gs.camera_pos[1]

        mp = pygame.mouse.get_pos()
        mx = mp[0]
        my = mp[1]

        center = (gs.resolution[0] / 2.0, gs.resolution[1] / 2.0)
        off_x = mx - center[0]
        off_x /= gs.resolution[0]

        off_y = my - center[1]
        off_y /= gs.resolution[1]

        x += dt * off_x * 1000.0
        y -= dt * off_y * 1000.0

        gs.camera_pos = (x, y)

        pass

    def upon_event(self, event: pygame.event):

        if event.type == pygame.QUIT:
            gs.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == ord("s"):
                spr = Sprite(load_image("Test.png"), position=(random.randrange(0, 500), random.randrange(0, 300)))

